from __future__ import annotations

from win32com import client

from pycommence.icommence._icommence_other import (
    App,
    CommenceDB,
    FormOA,
    FullControl,
    IApp,
    ICmcApplication,
    IConnOA,
    IControlOA,
    IDatabaseOA,
    IFieldOA,
    IFormOA,
    IFullControl,
    Isample,
    ISimple,
    IUIObj,
    Simple,
    UIObj,
    _DFormOAEvents,
    _IFullControlEvents,
    sample,
)
from pycommence.icommence.conversation import ICommenceConversation
from pycommence.icommence.cursor import ICommenceCursor
from pycommence.icommence.db import ICommenceDB
from pycommence.icommence.row import (
    ICommenceAddRowSet,
    ICommenceDeleteRowSet,
    ICommenceEditRowSet,
    ICommenceQueryRowSet,
)

# import win32com.client

IApp_vtables_dispatch_ = 1
IApp_vtables_ = [
    (
        (
            'Version',
            'bstrVersion',
        ),
        1,
        (
            1,
            (),
            [
                (16392, 10, None, None),
            ],
            1,
            1,
            4,
            0,
            56,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'GetCursor',
            'mode',
            'flag',
            'name',
        ),
        2,
        (
            2,
            (),
            [
                (3, 0, None, None),
                (3, 0, None, None),
                (16392, 10, None, None),
            ],
            1,
            1,
            4,
            0,
            64,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        ('quit',),
        3,
        (
            3,
            (),
            [],
            1,
            1,
            4,
            0,
            72,
            (3, 0, None, None),
            0,
        ),
    ),
]
IFullControl_vtables_dispatch_ = 1
IFullControl_vtables_ = [
    (
        (
            'myfunction',
            'x',
            'y',
        ),
        1,
        (
            1,
            (),
            [
                (3, 1, None, None),
                (3, 1, None, None),
            ],
            1,
            1,
            4,
            0,
            56,
            (3, 0, None, None),
            0,
        ),
    ),
]
ISimple_vtables_dispatch_ = 1
ISimple_vtables_ = [
    (
        ('Test',),
        1,
        (
            1,
            (),
            [],
            1,
            1,
            4,
            0,
            56,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Version',
            'bstrVersion',
        ),
        2,
        (
            2,
            (),
            [
                (16392, 10, None, None),
            ],
            1,
            1,
            4,
            0,
            64,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'MyEventCallback',
            'id',
            'pVarResult',
        ),
        3,
        (
            3,
            (),
            [
                (3, 0, None, None),
                (16396, 0, None, None),
            ],
            1,
            1,
            4,
            0,
            72,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Database',
            'pVal',
        ),
        4,
        (
            4,
            (),
            [
                (16393, 10, None, None),
            ],
            1,
            2,
            4,
            0,
            80,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Application',
            'pVal',
        ),
        5,
        (
            5,
            (),
            [
                (16393, 10, None, None),
            ],
            1,
            2,
            4,
            0,
            88,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Application',
            'pVal',
        ),
        5,
        (
            5,
            (),
            [
                (9, 1, None, None),
            ],
            1,
            4,
            4,
            0,
            96,
            (3, 0, None, None),
            0,
        ),
    ),
]
IUIObj_vtables_dispatch_ = 1
IUIObj_vtables_ = [
    (
        (
            'OnClick',
            'pdispBody',
            'varColor',
        ),
        1610743808,
        (
            1610743808,
            (),
            [
                (9, 1, None, None),
                (12, 1, None, None),
            ],
            1,
            1,
            4,
            0,
            56,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        ('HelloHTML',),
        1,
        (
            1,
            (),
            [],
            1,
            1,
            4,
            0,
            64,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        ('GoToURL',),
        2,
        (
            2,
            (),
            [],
            1,
            1,
            4,
            0,
            72,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Application',
            'pApp',
        ),
        3,
        (
            3,
            (),
            [
                (16393, 10, None, None),
            ],
            1,
            1,
            4,
            0,
            80,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'Test',
            'bstrVal',
        ),
        4,
        (
            4,
            (),
            [
                (16392, 10, None, None),
            ],
            1,
            1,
            4,
            0,
            88,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'GetTest',
            'bstrVal',
        ),
        5,
        (
            5,
            (),
            [
                (16392, 0, None, None),
            ],
            1,
            1,
            4,
            0,
            96,
            (3, 0, None, None),
            0,
        ),
    ),
    (
        (
            'clickIn',
            'x',
            'y',
        ),
        6,
        (
            6,
            (),
            [
                (3, 1, None, None),
                (3, 1, None, None),
            ],
            1,
            1,
            4,
            0,
            104,
            (3, 0, None, None),
            0,
        ),
    ),
]
Isample_vtables_dispatch_ = 1
Isample_vtables_ = []
RecordMap = {}
CLSIDToClassMap = {
    '{18884001-732C-11D0-AC0A-00A02485EC15}': ICmcApplication,
    '{383CFA14-73D5-11D0-AC0B-00A02485EC15}': IFieldOA,
    '{F180CB64-D4F0-464B-8EB6-0008689A24A6}': IControlOA,
    '{47A27291-7572-11D0-AC0B-00A02485EC15}': IConnOA,
    '{845A7A11-88F6-11D0-AC0E-00A02485EC15}': IDatabaseOA,
    '{654E7740-2AB6-11D0-8A93-444553540000}': IFormOA,
    '{654E7742-2AB6-11D0-8A93-444553540000}': _DFormOAEvents,
    '{654E7741-2AB6-11D0-8A93-444553540000}': FormOA,
    '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}': ICommenceCursor,
    '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}': ICommenceQueryRowSet,
    '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}': ICommenceAddRowSet,
    '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}': ICommenceEditRowSet,
    '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}': ICommenceDeleteRowSet,
    '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}': ICommenceConversation,
    '{92A04260-BE5C-11D1-99CC-00C04FD3695E}': ICommenceDB,
    '{92A04261-BE5C-11D1-99CC-00C04FD3695E}': CommenceDB,
    '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}': Isample,
    '{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}': sample,
    '{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}': _IFullControlEvents,
    '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}': IFullControl,
    '{789D254B-2D9B-487C-BABF-89D0EF6BD76C}': FullControl,
    '{1C9DF726-86D4-4C5B-8398-7418F0903597}': ISimple,
    '{DADC9CCF-FA28-4738-B142-B4CBD17267A6}': Simple,
    '{2BAE3CB5-A80C-11D4-A632-0040D0051497}': IUIObj,
    '{2BAE3CB6-A80C-11D4-A632-0040D0051497}': UIObj,
    '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}': IApp,
    '{9419F0A4-A8ED-11D4-824C-0050DAC366C6}': App,
}
CLSIDToPackageMap = {}
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}': 'Isample',
    '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}': 'IFullControl',
    '{1C9DF726-86D4-4C5B-8398-7418F0903597}': 'ISimple',
    '{2BAE3CB5-A80C-11D4-A632-0040D0051497}': 'IUIObj',
    '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}': 'IApp',
}
NamesToIIDMap = {
    'ICmcApplication': '{18884001-732C-11D0-AC0A-00A02485EC15}',
    'IFieldOA': '{383CFA14-73D5-11D0-AC0B-00A02485EC15}',
    'IControlOA': '{F180CB64-D4F0-464B-8EB6-0008689A24A6}',
    'IConnOA': '{47A27291-7572-11D0-AC0B-00A02485EC15}',
    'IDatabaseOA': '{845A7A11-88F6-11D0-AC0E-00A02485EC15}',
    'IFormOA': '{654E7740-2AB6-11D0-8A93-444553540000}',
    '_DFormOAEvents': '{654E7742-2AB6-11D0-8A93-444553540000}',
    'ICommenceCursor': '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceQueryRowSet': '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceAddRowSet': '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceEditRowSet': '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceDeleteRowSet': '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceConversation': '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}',
    'ICommenceDB': '{92A04260-BE5C-11D1-99CC-00C04FD3695E}',
    'Isample': '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}',
    '_IFullControlEvents': '{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}',
    'IFullControl': '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}',
    'ISimple': '{1C9DF726-86D4-4C5B-8398-7418F0903597}',
    'IUIObj': '{2BAE3CB5-A80C-11D4-A632-0040D0051497}',
    'IApp': '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}',
}
client.CLSIDToClass.RegisterCLSIDsFromDict(CLSIDToClassMap)
