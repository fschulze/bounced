from bounced import Bounce
try:
    from email import message_from_binary_file
except ImportError:
    from email import message_from_file as message_from_binary_file
from pkg_resources import resource_listdir
from pkg_resources import resource_stream
import os
import pytest


not_defined = object()


@pytest.fixture
def expected(request):
    expected = request.node.get_marker('expected').args[0]
    fn = request.node.funcargs['bounce_fn']
    fn = os.path.basename(fn).replace('.eml', '')
    return expected.get(fn, not_defined)


def pytest_generate_tests(metafunc):
    if 'bounce_fn' in metafunc.fixturenames:
        paths = [
            'tests/bounces',
            'tests/flufl_bounce',
            'tests/bounce_email/bounces',
            'tests/bounce_email/non_bounces']
        bounce_fns = []
        for path in paths:
            bounce_fns.extend(
                path + '/' + fn for fn in resource_listdir('bounced', path))
        bounce_fns = [
            fn for fn in bounce_fns
            if fn.endswith('.eml')]
        metafunc.parametrize('bounce_fn', sorted(bounce_fns))


def get_email(fn):
    with resource_stream('bounced', fn) as f:
        return message_from_binary_file(f)


@pytest.mark.expected({
    'aol_01': None,
    'bounce-auto-respond': None,
    'bounce_01': None, 'bounce_02': None, 'bounce_03': None,
    'dumbass_01': None,
    'exim_01': None,
    'groupwise_01': None, 'groupwise_02': None, 'groupwise_03': None,
    'hotpop_01': None,
    'llnl_01': None,
    'malformed_bounce_01': None,
    'microsoft_01': None, 'microsoft_02': None, 'microsoft_03': None,
    'newmailru_01': None,
    'postfix_01': None, 'postfix_02': None, 'postfix_03': None, 'postfix_04': None, 'postfix_05': None,
    'qmail_01': None, 'qmail_02': None, 'qmail_03': None, 'qmail_04': None, 'qmail_05': None, 'qmail_06': None, 'qmail_07': None, 'qmail_08': None,
    'sendmail_01': None,
    'simple_01': None, 'simple_02': None, 'simple_03': None, 'simple_04': None, 'simple_05': None, 'simple_06': None, 'simple_07': None, 'simple_08': None, 'simple_09': None, 'simple_10': None, 'simple_11': None, 'simple_12': None, 'simple_14': None, 'simple_15': None, 'simple_16': None, 'simple_17': None, 'simple_18': None, 'simple_19': None, 'simple_20': None, 'simple_21': None, 'simple_22': None, 'simple_23': None, 'simple_24': None, 'simple_25': None, 'simple_26': None, 'simple_27': None, 'simple_28': None, 'simple_29': None, 'simple_30': None, 'simple_32': None, 'simple_33': None, 'simple_34': None, 'simple_35': None, 'simple_36': None, 'simple_37': None, 'simple_38': None, 'simple_39': None, 'simple_40': None, 'simple_41': None,
    'sina_01': None,
    'smtp32_01': None, 'smtp32_02': None, 'smtp32_03': None, 'smtp32_04': None, 'smtp32_05': None, 'smtp32_06': None, 'smtp32_07': None,
    'tt_bounce_01': None, 'tt_bounce_02': None, 'tt_bounce_06': None, 'tt_bounce_08': None, 'tt_bounce_09': None, 'tt_bounce_11': None, 'tt_bounce_12_soft': None, 'tt_bounce_14': None, 'tt_bounce_17': None, 'tt_bounce_18': None, 'tt_bounce_19': None, 'tt_bounce_20': None, 'tt_bounce_21': None, 'tt_bounce_22': None, 'tt_bounce_25': None,
    'undeliverable_gmail': None,
    'unknown_code_bounce_01': None,
    'tt_1234210666': None, 'tt_1234211024': None, 'tt_1234241664': None,
    'yahoo_01': None, 'yahoo_02': None, 'yahoo_03': None, 'yahoo_04': None, 'yahoo_05': None, 'yahoo_06': None, 'yahoo_07': None, 'yahoo_08': None, 'yahoo_09': None, 'yahoo_10': None, 'yahoo_11': None,
    'yale_01': None})
def test_get_delivery_status(bounce_fn, expected):
    from bounced import DSN
    from bounced import get_delivery_status
    msg = get_email(bounce_fn)
    dsn = get_delivery_status(msg)
    if expected is None:
        assert dsn is None
        return
    assert isinstance(dsn, DSN)


@pytest.mark.expected({
    'dsn_01': [Bounce(
        ('', 'JimmyMcEgypt@sims-ms-daemon'),
        status='500',
        reporting_mta='msg00.seamail.go.com')],
    'dsn_02': [Bounce(
        ('', 'zzzzz@zeus.hud.ac.uk'),
        status='447')],
    'dsn_03': [Bounce(
        ('', 'ddd.kkk@advalvas.be'),
        action='failure',
        status='553')],
    'dsn_04': [Bounce(
        ('', 'HAASM@yogi.urz.unibas.ch'),
        status='500',
        reporting_mta='yogi.urz.unibas.ch')],
    'dsn_05': [Bounce(
        ('', 'pkocmid@atlas.cz'),
        action='delayed',
        status='441',
        reporting_mta='cuk.atlas.cz')],
    'dsn_06': [Bounce(
        ('', 'hao-nghi.au@fr.thalesgroup.com'),
        action='delayed',
        status='440',
        reporting_mta='gwsmtp.thomson-csf.com')],
    'dsn_07': [Bounce(
        ('', 'david.farrar@parliament.govt.nz'),
        action='delayed',
        status='441',
        reporting_mta='ns1.parliament.govt.nz')],
    'dsn_08': [Bounce(
        ('', 'news-list.zope@localhost.bln.innominate.de'),
        action='delayed',
        status='400',
        reporting_mta='mate.bln.innominate.de')],
    'dsn_09': [Bounce(
        ('', 'pr@allen-heath.com'),
        status='500')],
    'dsn_10': [Bounce(
        ('', 'anne.person@dom.ain'),
        status='500',
        reporting_mta='brainy.example.com')],
    'dsn_11': [Bounce(
        ('', 'joem@example.com'),
        status='511',
        reporting_mta='example.com')],
    'dsn_12': [Bounce(
        ('', 'auaauqdgrdz@jtc-con.co.jp'),
        status='511',
        reporting_mta='SV-03.jtc-con.local')],
    'dsn_13': [Bounce(
        ('', 'marcooherbst@cardinal.com'),
        status='511',
        reporting_mta='DUBCONN01.cahapps.net')],
    'dsn_14': [Bounce(
        ('', 'artboardregistration@home.dk'),
        status='550',
        reporting_mta='SMTP-GATEWAY01.intra.home.dk')],
    'dsn_15': [Bounce(
        ('', 'horu@ccc-ces.com'),
        status='511',
        reporting_mta='cccclyna01.ccc.coopcam.com')],
    'dsn_16': [Bounce(
        ('', 'hishealinghand@pastors.com'),
        status='500',
        reporting_mta='strategicnetwork.org')],
    'dsn_17': [Bounce(
        ('', 'kb3543.50@be37.mail.saunalahti.fi'),
        action='delayed',
        status='430',
        reporting_mta='be37.mail.saunalahti.fi')],
    'local-address': [Bounce(
        ('', 'recipient@example.com'),
        status='400')],
    'longer-status': [Bounce(
        ('', 'joem@example.com'),
        action='failed',
        status='5110',
        reporting_mta='example.com')],
    'tt_1234175799': [Bounce(
        ('', 'agris.ameriks@amerimailzzz.lv'),
        status='544',
        reporting_mta='Albanis-3.local')],
    'tt_1234177688': [Bounce(
        ('', 'aaaaagggrrriiiizz@inbox.lv'),
        status='554',
        reporting_mta='Albanis-3.local')],
    'tt_1234210655': [Bounce(
        ('', 'this_doesnotexistinAAc@accenture.com'),
        status='511',
        reporting_mta='mtahm1100.accenture.com')],
    'tt_1234211357': [Bounce(
        ('', 'agris.ameriksNEEXISTEE@gmail.com'),
        status='511',
        reporting_mta='Albanis-3.local')],
    'tt_1234211929': [Bounce(
        ('', 'jekaterina@tv5.lv'),
        status='523',
        reporting_mta='blackbird.grafton.lv')],
    'tt_1234211931': [Bounce(
        ('', 'info.rietumuradio.lv@mail.studio7.lv'),
        status='500',
        reporting_mta='mail.studio7pro.lv')],
    'tt_1234211932': [Bounce(
        ('', 'dace.balode@rigasvilni.lv'),
        status='550',
        reporting_mta='Albanis-3.local')],
    'tt_1234241665': [Bounce(
        ('', 'annas@sfl.lv'),
        status='550',
        reporting_mta='Albanis-3.local')],
    'tt_1234285532': [Bounce(
        ('', 'doesntexistthisemaill@yahoo.com'),
        status='554',
        reporting_mta='Albanis-3.local')],
    'tt_1234285668': [Bounce(
        ('', 'agrisa@one.lv'),
        status='552',
        reporting_mta='Albanis-3.local')],
    'tt_bounce_03': [Bounce(
        ('', 'agrisa@apollo.lv'),
        status='500',
        reporting_mta='apollo.lv')],
    'tt_bounce_04': [Bounce(
        ('', 'agrisa@apollo.lv'),
        status='500',
        reporting_mta='apollo.lv')],
    'tt_bounce_05': [Bounce(
        ('', 'evor@apollo.lv'),
        status='500',
        reporting_mta='smtp2.apollo.lv')],
    'tt_bounce_07': [Bounce(
        ('', 'ilona.kalnina@citrus.lv'),
        status='500',
        reporting_mta='avalon.telekom.lv')],
    'tt_bounce_10': [Bounce(
        ('', 'info.rietumuradio.lv@mail.studio7.lv'),
        status='400',
        reporting_mta='mail.studio7.lv')],
    'tt_bounce_13': [Bounce(
        ('', 'ilzeB@lvaei.lv'),
        status='522',
        reporting_mta='LVAEI-EXCH.lvaei.lv')],
    'tt_bounce_15': [Bounce(
        ('', 'info@rimibaltic.com'),
        status='500',
        reporting_mta='rimilt01.rimi.lan')],
    'tt_bounce_16': [Bounce(
        ('', 'jekaterina@tv5.lv'),
        status='523',
        reporting_mta='blackbird.grafton.lv')],
    'tt_bounce_23': [Bounce(
        ('', 'Rihards_Freimanis@exigengroup.com'),
        status='550',
        reporting_mta='pnew.exigengroup.lv')],
    'tt_bounce_24': [Bounce(
        ('', 'customer.testemail@test-receive-domain.se'),
        status='550',
        reporting_mta='test-receive-domain.se')],
    'netscape_01': set(),
    'simple_13': set(), 'simple_31': set(),
    'aol_01': None,
    'bounce-auto-respond': None,
    'bounce_01': None, 'bounce_02': None, 'bounce_03': None,
    'dumbass_01': None,
    'exim_01': None,
    'groupwise_01': None, 'groupwise_02': None, 'groupwise_03': None,
    'hotpop_01': None,
    'llnl_01': None,
    'malformed_bounce_01': None,
    'microsoft_01': None, 'microsoft_02': None, 'microsoft_03': None,
    'newmailru_01': None,
    'postfix_01': None, 'postfix_02': None, 'postfix_03': None, 'postfix_04': None, 'postfix_05': None,
    'qmail_01': None, 'qmail_02': None, 'qmail_03': None, 'qmail_04': None, 'qmail_05': None, 'qmail_06': None, 'qmail_07': None, 'qmail_08': None,
    'sendmail_01': None,
    'simple_01': None, 'simple_02': None, 'simple_03': None, 'simple_04': None, 'simple_05': None, 'simple_06': None, 'simple_07': None, 'simple_08': None, 'simple_09': None, 'simple_10': None, 'simple_11': None, 'simple_12': None, 'simple_14': None, 'simple_15': None, 'simple_16': None, 'simple_17': None, 'simple_18': None, 'simple_19': None, 'simple_20': None, 'simple_21': None, 'simple_22': None, 'simple_23': None, 'simple_24': None, 'simple_25': None, 'simple_26': None, 'simple_27': None, 'simple_28': None, 'simple_29': None, 'simple_30': None, 'simple_32': None, 'simple_33': None, 'simple_34': None, 'simple_35': None, 'simple_36': None, 'simple_37': None, 'simple_38': None, 'simple_39': None, 'simple_40': None, 'simple_41': None,
    'sina_01': None,
    'smtp32_01': None, 'smtp32_02': None, 'smtp32_03': None, 'smtp32_04': None, 'smtp32_05': None, 'smtp32_06': None, 'smtp32_07': None,
    'tt_bounce_01': None, 'tt_bounce_02': None, 'tt_bounce_06': None, 'tt_bounce_08': None, 'tt_bounce_09': None, 'tt_bounce_11': None, 'tt_bounce_12_soft': None, 'tt_bounce_14': None, 'tt_bounce_17': None, 'tt_bounce_18': None, 'tt_bounce_19': None, 'tt_bounce_20': None, 'tt_bounce_21': None, 'tt_bounce_22': None, 'tt_bounce_25': None,
    'undeliverable_gmail': None,
    'unknown_code_bounce_01': None,
    'tt_1234210666': None, 'tt_1234211024': None, 'tt_1234241664': None,
    'yahoo_01': None, 'yahoo_02': None, 'yahoo_03': None, 'yahoo_04': None, 'yahoo_05': None, 'yahoo_06': None, 'yahoo_07': None, 'yahoo_08': None, 'yahoo_09': None, 'yahoo_10': None, 'yahoo_11': None,
    'yale_01': None})
def test_bounces(bounce_fn, expected):
    from bounced import get_bounces
    msg = get_email(bounce_fn)
    result = get_bounces(msg)
    if isinstance(expected, list):
        for index, bounce in enumerate(sorted(result)):
            assert bounce.recipient == expected[index].recipient
            assert bounce.action == expected[index].action
            assert bounce.status == expected[index].status
            if expected[index].msg is not None:
                assert bounce.msg == expected[index].msg
            if expected[index].reporting_mta is not None:
                assert bounce.reporting_mta == expected[index].reporting_mta
    else:
        assert result == expected
