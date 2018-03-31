import attr
import email
import re


@attr.s(frozen=True)
class Bounce(object):
    recipient = attr.ib()
    status = attr.ib()
    action = attr.ib(default='failed')
    msg = attr.ib(default=None)
    reporting_mta = attr.ib(default=None)


@attr.s
class DSN(object):
    fields = attr.ib()
    original = attr.ib(default=None)


def get_message_rfc822(part):
    parts = part.get_payload()
    if len(parts) == 1:
        return parts[0]
    raise ValueError("message/rfc822 with multiple parts")


def get_delivery_status(msg):
    if not msg.is_multipart():
        return
    parts = msg.get_payload()
    if len(parts) < 2:
        return
    if len(parts) > 3:
        return
    if parts[1].get_content_type() != 'message/delivery-status':
        if msg.get_content_type() == 'multipart/report':
            return
        for part in msg.get_payload():
            if part.get_content_type() == 'message/rfc822':
                part = get_message_rfc822(part)
            dsn = get_delivery_status(part)
            if dsn is not None:
                return dsn
        return
    fields = []
    for field in parts[1].get_payload():
        if not len(field):
            continue
        fields.append(field)
    dsn = DSN(fields)
    if len(parts) == 3:
        if parts[2].get_content_type() == 'text/rfc822-headers':
            dsn.original = email.message_from_string(parts[2].get_payload())
        elif parts[2].get_content_type() == 'message/rfc822':
            dsn.original = get_message_rfc822(parts[2])
    return dsn


def get_recipient(field, name):
    recipient = field[name]
    addr_parts = recipient.split(';', 1)
    if len(addr_parts) == 1:
        return email.utils.parseaddr(addr_parts[0])
    elif len(addr_parts) == 2 and addr_parts[0].lower() == 'local':
        return email.utils.parseaddr(addr_parts[1])
    elif len(addr_parts) == 2 and addr_parts[0].lower() == 'rfc822':
        return email.utils.parseaddr(addr_parts[1])
    elif len(addr_parts) == 2 and addr_parts[0].lower() == 'x400':
        if not addr_parts[1].strip().startswith('/'):
            raise ValueError("Unknown x400 format for '%s' in DSN field: %s" % (name, recipient))
        parts = filter(None, addr_parts[1].strip().split('/'))
        parts = list(x.split('=', 1) for x in parts)
        parts = {k.lower(): v for k, v in parts}
        if 'rfc-822' in parts:
            return email.utils.parseaddr(parts['rfc-822'].replace('(a)', '@'))
        return
    elif len(addr_parts) == 2 and addr_parts[0].lower() == 'system':
        if addr_parts[1] == '<>':
            return
        raise ValueError("Unknown kind of '%s' in DSN field: %s" % (name, recipient))
    elif len(addr_parts) == 2:
        raise ValueError("Unknown kind of '%s' in DSN field: %s" % (name, recipient))
    raise ValueError("Invalid '%s' in DSN field: %s" % (name, recipient))


def get_action(field):
    if 'action' not in field:
        return
    action = field['action'].lower()
    action = action.split(None, 1)
    return action[0]


def get_diagnostic_code(field):
    if 'diagnostic-code' not in field:
        return
    dc_parts = field['diagnostic-code'].split(';', 1)
    if len(dc_parts) != 2:
        raise ValueError("Invalid Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
    if dc_parts[0].lower() != 'smtp':
        raise ValueError("Unknown kind of Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
    lines = list(x.strip() for x in dc_parts[1].splitlines())
    matcher = re.compile(r'(\d+)[\s\-]*(.*)$', re.DOTALL)
    matched = list(matcher.match(x) for x in lines)
    if any(x is None for x in matched):
        if matched[0] is None:
            raise ValueError("Malformed Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
        if any(x is not None for x in matched[1:]):
            raise ValueError("Malformed Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
        lines = ['\n'.join(lines)]
        matched = list(matcher.match(x) for x in lines)
        if matched[0] is None:
            raise ValueError("Malformed Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
    lines = list(x.groups() for x in matched)
    if len(set(x[0] for x in lines)) != 1:
        raise ValueError("Malformed Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
    code = lines[0][0]
    if len(code) != 3:
        raise ValueError("Malformed Diagnostic-Code in DSN field: %s" % field['diagnostic-code'])
    msg = '\n'.join(x[1] for x in lines)
    return (code, msg)


def get_final_recipient(field):
    if 'final-recipient' not in field:
        return
    return get_recipient(field, 'final-recipient')


def get_original_recipient(field):
    if 'original-recipient' not in field:
        return
    return get_recipient(field, 'original-recipient')


def get_reporting_mta(field):
    if 'reporting-mta' not in field:
        return
    rm_parts = field['reporting-mta'].split(';', 1)
    if len(rm_parts) == 1:
        return rm_parts[0].split(None, 1)[0]
    if len(rm_parts) != 2:
        raise ValueError("Invalid Reporting-MTA in DSN field: %s" % field['reporting-mta'])
    if rm_parts[0].lower() == 'dns':
        return rm_parts[1].split(None, 1)[0]
    elif rm_parts[0].lower() == 'x400':
        return
    raise ValueError("Unknown kind of Reporting-MTA in DSN field: %s" % field['reporting-mta'])


def get_status(field):
    if 'status' not in field:
        return
    status = field['status'].lower()
    status = status.split(None, 1)
    if '.' in status[0]:
        status[0] = status[0].split('.')
        if len(status[0]) != 3:
            raise ValueError("Malformed Status in DSN field: %s" % field['status'])
        status[0] = ''.join(status[0])
    if len(status) == 1:
        status.append('')
    if len(status) != 2:
        raise ValueError("Malformed Status in DSN field: %s" % field['status'])
    return tuple(status)


def get_bounces(msg):
    dsn = get_delivery_status(msg)
    if dsn is None:
        return
    bounces = set()
    reporting_mta = None
    for field in dsn.fields:
        final_recipient = get_final_recipient(field)
        if final_recipient is None:
            if 'reporting-mta' in field:
                if reporting_mta is not None:
                    raise ValueError
                reporting_mta = get_reporting_mta(field)
                continue
            if 'last-attempt-date' in field:
                continue
            final_recipient = get_original_recipient(field)
            if final_recipient is None:
                continue
        action = get_action(field)
        status = get_status(field)
        if status is not None:
            (status, msg) = status
        try:
            diagnostic_code = get_diagnostic_code(field)
            if diagnostic_code is not None:
                (status, msg) = diagnostic_code
        except ValueError:
            pass
        bounces.add(Bounce(
            recipient=final_recipient,
            action=action,
            status=status,
            msg=msg,
            reporting_mta=reporting_mta))
    return bounces
