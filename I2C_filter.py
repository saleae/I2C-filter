# High Level Analyzer
# For more information and documentation, please go to https://github.com/saleae/logic2-examples
from typing import Optional

TARGET_KEY = 'Target Address (Dec or Hex)'


class Hla():
    current_address: int
    target_address: int

    def __init__(self):
        '''
        '''
        pass

    def get_capabilities(self):
        '''
        Set the target address as decimal or hex
        '''
        return {
            'settings': {
                TARGET_KEY: {
                    'type': 'string'
                }
            }
        }

    def set_settings(self, settings):
        '''
        '''
        target_address = settings.get(TARGET_KEY)
        if not target_address:
            raise Exception('Target address is missing')

        base = 16 if target_address.startswith('0x') else 10
        try:
            self.target_address = int(target_address, base)
        except Exception as e:
            raise Exception('Invalid target address')

        return {
            'result_types': {
                'default': {
                    'format': '{{data.value}}, {{data.type}}'
                }
            }
        }

    def decode(self, frame):
        '''
        '''
        value = None
        if frame['type'] == 'address':
            address = frame['data']['address'][0]
            read_write_bit = (address & 0x01)  # Read = 1
            address -= read_write_bit
            self.current_address = address

        if frame['type'] != 'data':
            return None

        if self.current_address == self.target_address:
            value = frame['data']['address'][0] if frame['type'] == 'address' else frame['data']['data'][0]
            return {
                'type': 'default',
                'start_time': frame['start_time'],
                'end_time': frame['end_time'],
                'data': {
                    'type': frame['type'],
                    'value': value
                }
            }

        return None
