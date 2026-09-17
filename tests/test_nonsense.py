from pycommence import PyCommence
from pycommence.core.filters import ConditionType, FieldFilter
from pycommence.dde import DDEKind, DDETopic
from pycommence.dde.msgs import execute, view


def view_shipment(barcode: str):
    with PyCommence() as p:
        conv = p.conversation(DDETopic.VIEW)

        msg = view.category('Shipment')
        p.send_dde_message(msg)

        msg = execute.show_view('Shipment Grid')
        res = p.send_dde_message(msg)

        fil = FieldFilter(column='Latest Tracking', value=barcode, condition=ConditionType.CONTAIN)
        # fil_text ='[ViewFilter(1, F, "", "Latest Tracking", Contains, FI951663272GB)]'
        fil_text = fil.view_filter_str(1)
        res = conv.send_message_text_req(fil_text)

        # params = fil._filter_str.split(',')
        # params = [_.replace('"', '').replace(' ', '') for _ in params]
        # msg = view.filter_(1, fil.kind, '', *params)
        # p.send_dde_message(msg)

        # fil_text = fil.view_filter_str()
        # fil_text = '[ViewFilter(1, F,, "Latest Tracking Link", "Contains", "FI951663272GB", )]'


def view_contact_2(name_str: str):
    with PyCommence() as p:
        # conv = p.conversation(DDETopic.VIEW)
        showy = execute.show_item('Contact', name_str, topic=DDETopic.VIEW, form_name='Contact')
        p.send_dde_message(showy)


def view_contact(name_str: str):
    with PyCommence() as p:
        conv = p.conversation(DDETopic.VIEW)

        msg = view.category('Contact')
        p.send_dde_message(msg)

        show_msg = execute.show_view('Contact List')
        res = p.send_dde_message(show_msg)

        fil = FieldFilter(column='contactKey', value=name_str, condition=ConditionType.CONTAIN)
        # fil_text ='[ViewFilter(1, F, "", "Latest Tracking", Contains, FI951663272GB)]'
        fil_text = fil.view_filter_str(1)
        res = conv.send_message_text_req(fil_text)

        # showy = execute.show_item('Contact', 'Bezos.Jeff', topic=DDETopic.VIEW, form_name='Contact')
        # p.send_dde_message(showy)

        # params = fil._filter_str.split(',')
        # params = [_.replace('"', '').replace(' ', '') for _ in params]
        # msg = view.filter_(1, fil.kind, '', *params)
        # p.send_dde_message(msg)

        # fil_text = fil.view_filter_str()
        # fil_text = '[ViewFilter(1, F,, "Latest Tracking Link", "Contains", "FI951663272GB", )]'

    ...


def test_non():
    # view_shipment('FI951663272GB')
    view_contact_2('Bezos.Jeff')
