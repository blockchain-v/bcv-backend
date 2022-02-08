from openapi_server.contract import contract
from openapi_server.repositories import User, Nonce
from .authService import check_auth
from openapi_server.services import smartContractService

import logging
from mongoengine import DoesNotExist
from operator import itemgetter

log = logging.getLogger('userService')


class UserService:

    @staticmethod
    def register(event_args_dict):
        """
        Registers a user in the db collection 'user'
        :param event_args_dict:
        :return:
        """
        try:
            new_user_address, signed_address = itemgetter('user', 'signedAddress')(event_args_dict)
            log.info(f'is register {new_user_address}, {signed_address}')
            auth_status = False
            if check_auth(claim=new_user_address, signed_claim=signed_address):
                log.info('checkauth passed')
                user = User(address=new_user_address)
                user.save()
                auth_status = True
            else:
                log.info('newUserAddress != address')
            # SC callback to report status of the registration (successful/unsuccessful)
            smartContractService.service.report_registration_to_sc(new_user_address, auth_status)
        except Exception as e:
            log.info(f'register error {e}')
            # SC callback called with success as False
            smartContractService.service.report_registration_to_sc(new_user_address, False)

    @staticmethod
    def unregister(event_args_dict):
        """
        Deletes a user from the db collection 'user' and the associated nonce, if exists
        :param event_args_dict:
        :return:
        """
        try:
            user_address = itemgetter('user')(event_args_dict)
            log.info(f'unregister {user_address}')
            user_to_delete = User.objects(address=user_address)
            user_len = len(user_to_delete)
            user_to_delete.delete()
            nonce_to_delete = Nonce.objects(address=user_address)
            nonce_to_delete.delete()
            # SC callback to report status of the registration (successful/unsuccessful)
            # success is false if no users were found to be deleted (i.e. not yet registered)
            smartContractService.service.report_unregistration_to_sc(user_address, user_len > 0)

        except Exception as e:
            log.info(f'unregister error {e}')
            # SC callback called with success as False
            smartContractService.service.report_unregistration_to_sc(contract, user_address, False)

    @staticmethod
    def is_user_registered(address) -> bool:
        """
        Checks if a user with the given address has been registered
        :param address:
        :return:  boolean
        """
        try:
            User.objects.get(address=address)
            return True
        except DoesNotExist:
            return False


service = UserService()
