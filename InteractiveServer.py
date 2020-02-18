import json
from Command.Error import NotFoundCommand
from Command.IU import IU
from Module.LineBot import LineNotify

command_dictionary = {
    # 'insert_token': InsertToken
    '/iu': IU
}


class CommandExecutor:
    def __init__(self):
        self.execute_finished = False

    def execute(self, command_json):
        try:

            command, parameter, replyToken = CommandAndParameterGenerator().get_command_and_parameter(str(command_json))
            command = CommandAvailabilityChecker().check(command, parameter)

            self.__execute_command(command, parameter, replyToken)

        except Exception as e:
            error_message = 'CommandExecutor execute: {}'.format(e)
            LineNotify(access_token="VuNI0a99OAJCVtLkfC03TDozVi2HgsregB7vjLgeyQm").send(error_message)

    def __execute_command(self, command, parameter, replyToken):
        if command != 'Error':
            command_instance = command_dictionary[command]
            command_instance(parameter, replyToken).execute()
        else:
            NotFoundCommand(replyToken).execute()
            LineNotify(access_token="VuNI0a99OAJCVtLkfC03TDozVi2HgsregB7vjLgeyQm").send('無此指令')

class CommandAndParameterGenerator:
    @staticmethod
    def get_command_and_parameter(command_json):
        command_dict = json.loads(command_json)
        replyToken = command_dict['replyToken']
        message = command_dict['message']['text'].split()
        command = message[0]
        try:
            parameter = message[1]
        except:
            parameter = ''

        # command = command_dict['command']
        # parameter = command_dict['parameter']

        return command, parameter, replyToken

class CommandAvailabilityChecker:
    @staticmethod
    def check(command, parameter):
        if command not in command_dictionary.keys():
            # raise CommandNotFoundError
            return 'Error'

if __name__ == "__main__":
    message = '{"message": {"id": "11452795300826", "text": "IX", "type": "text"}, "replyToken": "db2f11e55f604a9b810971bf6f419b82", "source": {"type": "user", "userId": "U643c363fb1c41c4e9109ed48322d784c"}, "timestamp": 1582034792190, "type": "message"}'
    CommandExecutor().execute(command_json=message)