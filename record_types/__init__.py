
from collections import namedtuple


BLPU = namedtuple('BLPU', [
    'RECORD_IDENTIFIER', 'CHANGE_TYPE', 'PRO_ORDER','UPRN', 'LOGICAL_STATUS',
    'BLPU_STATE', 'BLPU_STATE_DATE', 'PARENT_UPRN', 'X_COORDINATE',
    'Y_COORDINATE', 'RPC', 'LOCAL_CUSTODIAN_CODE', 'START_DATE', 'END_DATE',
    'LAST_UPDATE_DATE', 'ENTRY_DATE', 'POSTAL_ADDRESS', 'POSTCODE_LOCATOR',
    'MULTI_OCC_COUNT']
)

DPA = namedtuple('DPA', [
    'RECORD_IDENTIFIER', 'CHANGE_TYPE', 'PRO_ORDER', 'UPRN',
    'PARENT_ADDRESSABLE_UPRN', 'RM_UDPRN', 'ORGANISATION_NAME',
    'DEPARTMENT_NAME', 'SUB_BUILDING_NAME', 'BUILDING_NAME', 'BUILDING_NUMBER',
    'DEPENDENT_THOROUGHFARE_NAME', 'THOROUGHFARE_NAME',
    'DOUBLE_DEPENDENT_LOCALITY', 'DEPENDENT_LOCALITY', 'POST_TOWN', 'POSTCODE',
    'POSTCODE_TYPE', 'WELSH_DEPENDENT_THOROUGHFARE_NAME',
    'WELSH_THOROUGHFARE_NAME', 'WELSH_DOUBLE_DEPENDENT_LOCALITY',
    'WELSH_DEPENDENT_LOCALITY', 'WELSH_POST_TOWN', 'PO_BOX_NUMBER',
    'PROCESS_DATE', 'START_DATE', 'END_DATE', 'LAST_UPDATE_DATE', 'ENTRY_DATE']
)
