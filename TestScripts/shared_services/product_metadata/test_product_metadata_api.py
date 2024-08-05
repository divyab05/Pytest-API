import inspect
import json
import os
import random
import pytest
import logging
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.generic_utils import generate_random_string
from hamcrest import assert_that, equal_to


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    prod_md = {
        'app_config': app_config,
        'prod_md': ProductMetadata(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config)
    }
    yield prod_md


@pytest.mark.usefixtures('initialize')
class TestProductMetadataAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('PROD_METADATA', 'sample_get_prod_details_resp')) as f1:
            self.sample_get_prod_details_resp = json.load(f1)

        with open(self.prop.get('PROD_METADATA', 'sample_get_prod_count_resp')) as f2:
            self.sample_get_prod_count_resp = json.load(f2)

        with open(self.prop.get('PROD_METADATA', 'sample_created_prod_resp')) as f3:
            self.sample_created_prod_resp = json.load(f3)

        with open(self.prop.get('PROD_METADATA', 'sample_get_spss_prod_details_resp')) as f4:
            self.sample_get_spss_prod_details_resp = json.load(f4)

        with open(self.prop.get('PROD_METADATA', 'sample_get_carrier_details_resp')) as f5:
            self.sample_get_carrier_details_resp = json.load(f5)

        with open(self.prop.get('PROD_METADATA', 'sample_get_carrier_count_resp')) as f6:
            self.sample_get_carrier_count_resp = json.load(f6)

        with open(self.prop.get('PROD_METADATA', 'sample_created_carrier_resp')) as f7:
            self.sample_created_carrier_resp = json.load(f7)

        with open(self.prop.get('PROD_METADATA', 'sample_country_codes_resp')) as f8:
            self.sample_country_codes_resp = json.load(f8)

        with open(self.prop.get('PROD_METADATA', 'sample_created_feature_resp')) as f9:
            self.sample_created_feature_resp = json.load(f9)

        with open(self.prop.get('PROD_METADATA', 'sample_get_feature_details_resp')) as f10:
            self.sample_get_feature_details_resp = json.load(f10)

        with open(self.prop.get('PROD_METADATA', 'sample_get_feature_count_resp')) as f11:
            self.sample_get_feature_count_resp = json.load(f11)

        with open(self.prop.get('PROD_METADATA', 'sample_created_plan_resp')) as f12:
            self.sample_created_plan_resp = json.load(f12)

        with open(self.prop.get('PROD_METADATA', 'sample_get_plan_details_resp')) as f13:
            self.sample_get_plan_details_resp = json.load(f13)

        with open(self.prop.get('PROD_METADATA', 'sample_get_plans_count_resp')) as f13:
            self.sample_get_plans_count_resp = json.load(f13)

        with open(self.prop.get('PROD_METADATA', 'sample_get_plan_feature_resp')) as f14:
            self.sample_get_plan_feature_resp = json.load(f14)

        with open(self.prop.get('PROD_METADATA', 'sample_get_role_template_details_resp')) as f15:
            self.sample_get_role_template_details_resp = json.load(f15)

        with open(self.prop.get('PROD_METADATA', 'sample_get_role_templates_count_resp')) as f16:
            self.sample_get_role_templates_count_resp = json.load(f16)

        with open(self.prop.get('PROD_METADATA', 'sample_created_role_template_resp')) as f17:
            self.sample_created_role_template_resp = json.load(f17)

        with open(self.prop.get('PROD_METADATA', 'sample_get_admin_role_details_resp')) as f18:
            self.sample_get_admin_role_details_resp = json.load(f18)

        with open(self.prop.get('PROD_METADATA', 'sample_created_admin_roles_resp')) as f19:
            self.sample_created_admin_roles_resp = json.load(f19)

        with open(self.prop.get('PROD_METADATA', 'sample_admin_roles_by_group_name_resp')) as f20:
            self.sample_admin_roles_by_group_name_resp = json.load(f20)

        with open(self.prop.get('PROD_METADATA', 'sample_get_hub_details_resp')) as f21:
            self.sample_get_hub_details_resp = json.load(f21)

        with open(self.prop.get('PROD_METADATA', 'sample_get_hubs_count_resp')) as f22:
            self.sample_get_hubs_count_resp = json.load(f22)

        with open(self.prop.get('PROD_METADATA', 'sample_created_hub_resp')) as f23:
            self.sample_created_hub_resp = json.load(f23)

        with open(self.prop.get('PROD_METADATA', 'sample_postage_value_details_resp')) as f24:
            self.sample_postage_value_details_resp = json.load(f24)

        with open(self.prop.get('PROD_METADATA', 'sample_created_postage_value_resp')) as f25:
            self.sample_created_postage_value_resp = json.load(f25)

        with open(self.prop.get('PROD_METADATA', 'sample_integrator_details_resp')) as f26:
            self.sample_integrator_details_resp = json.load(f26)

        with open(self.prop.get('PROD_METADATA', 'sample_created_locale_resp')) as f27:
            self.sample_created_locale_resp = json.load(f27)

        with open(self.prop.get('PROD_METADATA', 'sample_locale_details_resp')) as f28:
            self.sample_locale_details_resp = json.load(f28)

        with open(self.prop.get('PROD_METADATA', 'sample_get_locales_count_resp')) as f29:
            self.sample_get_locales_count_resp = json.load(f29)

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_01_verify_get_product_details_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_prod_details_resp = resource['prod_md'].get_product_details_from_token_api()
        assert_that(self.compare_response_objects(get_prod_details_resp.json()[0], self.sample_get_prod_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_02_verify_get_product_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_prod_count_resp = resource['prod_md'].get_product_count_from_token_api()
        assert_that(self.validate_response_template(get_prod_count_resp, self.sample_get_prod_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_03_verify_get_product_details_by_prod_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_prod_details_resp = resource['prod_md'].get_product_details_by_prod_id_api(prod_id='SPA')
        assert_that(self.validate_response_template(get_prod_details_resp, self.sample_get_prod_details_resp, 200))
        assert_that(get_prod_details_resp.json()['productID'], equal_to('SPA'))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_04_verify_create_update_archive_product(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        prod_id = generate_random_string(lowercase=False, char_count=6)
        name = generate_random_string(char_count=20)

        # Check and delete if the product id exists
        resource['prod_md'].check_and_delete_product_by_prod_id(prod_id=prod_id)

        # Create product
        create_prod_resp = resource['prod_md'].post_create_product_api(prod_id=prod_id, name=name)
        assert_that(self.validate_response_template(create_prod_resp, self.sample_created_prod_resp, 201))
        assert_that(create_prod_resp.json()['productID'], equal_to(prod_id))

        try:
            # Update product name
            update_name = generate_random_string()
            update_prod_resp = resource['prod_md'].put_update_product_by_prod_id_api(prod_id=prod_id, name=update_name)
            assert_that(self.validate_response_code(update_prod_resp, 200))

            get_prod_resp = resource['prod_md'].get_product_details_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_template(get_prod_resp, self.sample_get_spss_prod_details_resp, 200))
            assert_that(get_prod_resp.json()['name'], equal_to(update_name))

        finally:
            # Archive product name
            archive_prod_resp = resource['prod_md'].put_archive_product_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_code(archive_prod_resp, 200))

            get_prod_after_archive_resp = resource['prod_md'].get_product_details_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_code(get_prod_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_05_verify_create_update_delete_product(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        prod_id = generate_random_string(lowercase=False, char_count=6)
        name = generate_random_string(char_count=20)

        # Check and delete if the product id exists
        resource['prod_md'].check_and_delete_product_by_prod_id(prod_id=prod_id)

        # Create product
        create_prod_resp = resource['prod_md'].post_create_product_api(prod_id=prod_id, name=name)
        assert_that(self.validate_response_template(create_prod_resp, self.sample_created_prod_resp, 201))
        assert_that(create_prod_resp.json()['productID'], equal_to(prod_id))

        try:
            # Update product name
            update_name = generate_random_string()
            update_prod_resp = resource['prod_md'].put_update_product_by_prod_id_api(prod_id=prod_id, name=update_name)
            assert_that(self.validate_response_code(update_prod_resp, 200))

            get_prod_resp = resource['prod_md'].get_product_details_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_template(get_prod_resp, self.sample_get_spss_prod_details_resp, 200))
            assert_that(get_prod_resp.json()['name'], equal_to(update_name))

        finally:
            # Delete product name
            del_prod_resp = resource['prod_md'].del_product_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_code(del_prod_resp, 200))

            get_prod_after_del_resp = resource['prod_md'].get_product_details_by_prod_id_api(prod_id=prod_id)
            assert_that(self.validate_response_code(get_prod_after_del_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skip("Carrier APIs are removed and few are moved to config-service. Jira Ticket: PE-4040")
    def test_06_verify_get_carrier_details_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_carrier_details_resp = resource['prod_md'].get_carriers_from_token_api()
        assert_that(self.compare_response_objects(get_carrier_details_resp.json()[0],
                                                  self.sample_get_carrier_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skip("Carrier APIs are removed and few are moved to config-service. Jira Ticket: PE-4040")
    def test_07_verify_get_carrier_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_carrier_count_resp = resource['prod_md'].get_carriers_count_from_token_api()
        assert_that(self.validate_response_template(get_carrier_count_resp, self.sample_get_carrier_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skip("Carrier APIs are removed and few are moved to config-service. Jira Ticket: PE-4040")
    def test_08_verify_get_carrier_details_by_carrier_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_carrier_details_resp = resource['prod_md'].get_carrier_details_by_carrier_id_api(carrier_id='USPS')
        assert_that(self.validate_response_template(get_carrier_details_resp, self.sample_get_carrier_details_resp, 200))
        assert_that(get_carrier_details_resp.json()['carrierID'], equal_to('USPS'))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    @pytest.mark.skip("Carrier APIs are removed and few are moved to config-service. Jira Ticket: PE-4040")
    def test_09_verify_create_update_archive_carrier(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        carrier_id = generate_random_string(lowercase=False, char_count=6)
        name = generate_random_string(char_count=20)

        # Check and delete if the carrier id exists
        resource['prod_md'].check_and_delete_carrier_by_carrier_id(carrier_id=carrier_id)

        # Create carrier
        create_carrier_resp = resource['prod_md'].post_create_carrier_api(carrier_id=carrier_id, name=name)
        assert_that(self.validate_response_template(create_carrier_resp, self.sample_created_carrier_resp, 201))
        assert_that(create_carrier_resp.json()['carrierID'], equal_to(carrier_id))

        try:
            # Update carrier name
            update_name = generate_random_string()
            update_carrier_resp = resource['prod_md'].put_update_carrier_by_carrier_id_api(carrier_id=carrier_id, name=update_name)
            assert_that(self.validate_response_code(update_carrier_resp, 200))

            get_carrier_resp = resource['prod_md'].get_carrier_details_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_template(get_carrier_resp, self.sample_get_carrier_details_resp, 200))
            assert_that(get_carrier_resp.json()['name'], equal_to(update_name))

        finally:
            # Archive carrier name
            archive_carrier_resp = resource['prod_md'].put_archive_carrier_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_code(archive_carrier_resp, 200))

            get_carrier_after_archive_resp = resource['prod_md'].get_carrier_details_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_code(get_carrier_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skip("Carrier APIs are removed and few are moved to config-service. Jira Ticket: PE-4040")
    def test_10_verify_create_update_delete_carrier(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        carrier_id = generate_random_string(lowercase=False, char_count=6)
        name = generate_random_string(char_count=20)

        # Check and delete if the carrier id exists
        resource['prod_md'].check_and_delete_carrier_by_carrier_id(carrier_id=carrier_id)

        # Create carrier
        create_carrier_resp = resource['prod_md'].post_create_carrier_api(carrier_id=carrier_id, name=name)
        assert_that(self.validate_response_template(create_carrier_resp, self.sample_created_carrier_resp, 201))
        assert_that(create_carrier_resp.json()['carrierID'], equal_to(carrier_id))

        try:
            # Update carrier name
            update_name = generate_random_string()
            update_carrier_resp = resource['prod_md'].put_update_carrier_by_carrier_id_api(carrier_id=carrier_id, name=update_name)
            assert_that(self.validate_response_code(update_carrier_resp, 200))

            get_carrier_resp = resource['prod_md'].get_carrier_details_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_template(get_carrier_resp, self.sample_get_carrier_details_resp, 200))
            assert_that(get_carrier_resp.json()['name'], equal_to(update_name))

        finally:
            # Delete carrier name
            del_carrier_resp = resource['prod_md'].del_carrier_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_code(del_carrier_resp, 200))

            get_carrier_after_del_resp = resource['prod_md'].get_carrier_details_by_carrier_id_api(carrier_id=carrier_id)
            assert_that(self.validate_response_code(get_carrier_after_del_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_11_verify_get_country_codes(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_country_codes_resp = resource['prod_md'].get_country_codes_api()
        assert_that(
            self.validate_response_template(get_country_codes_resp, self.sample_country_codes_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_12_verify_get_feature_details_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_feature_details_resp = resource['prod_md'].get_features_from_token_api()
        assert_that(self.compare_response_objects(get_feature_details_resp.json()[0],
                                                  self.sample_get_feature_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_13_verify_get_feature_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_feature_count_resp = resource['prod_md'].get_features_count_from_token_api()
        assert_that(self.validate_response_template(get_feature_count_resp, self.sample_get_feature_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_14_verify_get_feature_details_by_ft_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_feature_details_resp = resource['prod_md'].get_feature_details_by_ft_id_api(ft_id='SHIPPING_HISTORY')
        assert_that(
            self.validate_response_template(get_feature_details_resp, self.sample_get_feature_details_resp, 200))
        assert_that(get_feature_details_resp.json()['featureID'], equal_to('SHIPPING_HISTORY'))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_15_verify_create_update_archive_feature(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        ft_id = generate_random_string(lowercase=False)
        name = generate_random_string()
        funct_tag = generate_random_string()
        resource_value = generate_random_string()
        operations = ['GET']
        countries = ['AU', 'CA', 'GB', 'US']

        # Check and delete if the feature id exists
        resource['prod_md'].check_and_delete_feature_by_ft_id(ft_id=ft_id)

        # Create feature
        create_feature_resp = resource['prod_md']\
            .post_create_feature_api(ft_id=ft_id, name=name, funct_tag=funct_tag, resource_value=resource_value,
                                     operations=operations, supported_countries=countries)
        assert_that(self.validate_response_template(create_feature_resp, self.sample_created_feature_resp, 201))
        assert_that(create_feature_resp.json()['featureID'], equal_to(ft_id))

        try:
            # Update feature name
            update_name = 'SPSS Auto Test Updated'
            update_feature_resp = resource['prod_md']\
                .put_update_feature_by_ft_id_api(ft_id=ft_id, name=update_name, funct_tag=funct_tag,
                                                 resource_value=resource_value, operations=operations,
                                                 supported_countries=countries)
            assert_that(self.validate_response_code(update_feature_resp, 200))

            get_feature_resp = resource['prod_md'].get_feature_details_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_template(get_feature_resp, self.sample_get_feature_details_resp, 200))
            assert_that(get_feature_resp.json()['name'], equal_to(update_name))

        finally:
            # Archive feature name
            archive_feature_resp = resource['prod_md'].put_archive_feature_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_code(archive_feature_resp, 200))

            get_feature_after_archive_resp = resource['prod_md'].get_feature_details_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_code(get_feature_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_16_verify_create_update_delete_feature(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        ft_id = generate_random_string(lowercase=False)
        name = generate_random_string()
        funct_tag = generate_random_string()
        resource_value = generate_random_string()
        operations = ['GET']
        countries = ['AU', 'CA', 'GB', 'US']

        # Check and delete if the feature id exists
        resource['prod_md'].check_and_delete_feature_by_ft_id(ft_id=ft_id)

        # Create feature
        create_feature_resp = resource['prod_md'] \
            .post_create_feature_api(ft_id=ft_id, name=name, funct_tag=funct_tag, resource_value=resource_value,
                                     operations=operations, supported_countries=countries)
        assert_that(self.validate_response_template(create_feature_resp, self.sample_created_feature_resp, 201))
        assert_that(create_feature_resp.json()['featureID'], equal_to(ft_id))

        try:
            # Update feature name
            update_name = 'SPSS Auto Test Updated'
            update_feature_resp = resource['prod_md'] \
                .put_update_feature_by_ft_id_api(ft_id=ft_id, name=update_name, funct_tag=funct_tag,
                                                 resource_value=resource_value, operations=operations,
                                                 supported_countries=countries)
            assert_that(self.validate_response_code(update_feature_resp, 200))

            get_feature_resp = resource['prod_md'].get_feature_details_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_template(get_feature_resp, self.sample_get_feature_details_resp, 200))
            assert_that(get_feature_resp.json()['name'], equal_to(update_name))

        finally:
            # Delete feature name
            del_feature_resp = resource['prod_md'].del_feature_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_code(del_feature_resp, 200))

            get_feature_after_del_resp = resource['prod_md'].get_feature_details_by_ft_id_api(ft_id=ft_id)
            assert_that(self.validate_response_code(get_feature_after_del_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_17_verify_get_plans_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_plans_resp = resource['prod_md'].get_plans_from_token_api()
        assert_that(self.compare_response_objects(get_plans_resp.json()[0],
                                                  self.sample_get_plan_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_18_verify_get_plans_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_plans_count_resp = resource['prod_md'].get_plans_count_from_token_api()
        assert_that(self.validate_response_template(get_plans_count_resp, self.sample_get_plans_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_19_verify_get_plan_details_by_plan_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_plan_details_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id='SENDING_PLAN')
        assert_that(
            self.validate_response_template(get_plan_details_resp, self.sample_get_plan_details_resp, 200))
        assert_that(get_plan_details_resp.json()['planID'], equal_to('SENDING_PLAN'))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_20_verify_get_plan_features_by_plan_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_plan_features_resp = resource['prod_md'].get_plan_features_by_plan_id_api(plan_id='SENDING_PLAN')
        assert_that(self.compare_response_objects(get_plan_features_resp.json()[0],
                                                  self.sample_get_plan_feature_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_21_verify_get_plan_details_by_plan_ids(self, resource, app_config):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        plan_ids = ['PITNEYSHIP', 'SENDING_PLAN']

        get_plan_details_resp = resource['prod_md'].post_get_plans_by_plan_ids_api(plan_ids=plan_ids)
        assert_that(self.compare_response_objects(get_plan_details_resp.json()[0],
                                                  self.sample_get_plan_details_resp))

        if app_config.env_cfg['product_name'] == 'sp360commercial':
            assert_that(get_plan_details_resp.json()[0]['planID'], equal_to('PITNEYSHIP'))
            assert_that(get_plan_details_resp.json()[1]['planID'], equal_to('SENDING_PLAN'))
        elif app_config.env_cfg['product_name'] == 'fedramp':
            assert_that(get_plan_details_resp.json()[0]['planID'], equal_to('SENDING_PLAN'))
            assert_that(get_plan_details_resp.json()[1]['planID'], equal_to('PITNEYSHIP'))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_22_verify_create_update_archive_plan(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        plan_id, name, desc, status, features = resource['prod_md'].create_plan_data(archive_plan=True)

        # Create plan
        create_plan_resp = resource['prod_md'] \
            .post_create_plan_api(plan_id=plan_id, name=name, desc=desc, status=status, features=features)
        assert_that(self.validate_response_template(create_plan_resp, self.sample_created_plan_resp, 201))
        assert_that(create_plan_resp.json()['planID'], equal_to(plan_id))

        try:
            # Update plan name
            updated_name = generate_random_string()
            updated_features = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER', 'VIEW_CONTACTS']
            update_plan_resp = resource['prod_md'] \
                .put_update_plan_api(plan_id=plan_id, name=updated_name, desc=desc, status=status, features=updated_features)
            assert_that(self.validate_response_code(update_plan_resp, 200))

            get_plan_details_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_template(get_plan_details_resp, self.sample_get_plan_details_resp, 200))
            assert_that(get_plan_details_resp.json()['name'], equal_to(updated_name))
            assert_that(get_plan_details_resp.json()['features'], equal_to(updated_features))

        finally:
            # Archive plan name
            archive_plan_resp = resource['prod_md'].put_archive_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(archive_plan_resp, 200))

            get_plan_after_archive_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(get_plan_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_23_verify_create_update_delete_plan(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        plan_id, name, desc, status, features = resource['prod_md'].create_plan_data()

        # Create plan
        create_plan_resp = resource['prod_md'] \
            .post_create_plan_api(plan_id=plan_id, name=name, desc=desc, status=status, features=features)
        assert_that(self.validate_response_template(create_plan_resp, self.sample_created_plan_resp, 201))
        assert_that(create_plan_resp.json()['planID'], equal_to(plan_id))

        try:
            # Update plan name
            updated_name = generate_random_string()
            updated_features = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER', 'VIEW_CONTACTS']
            update_plan_resp = resource['prod_md'] \
                .put_update_plan_api(plan_id=plan_id, name=updated_name, desc=desc, status=status,
                                     features=updated_features)
            assert_that(self.validate_response_code(update_plan_resp, 200))

            get_plan_details_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_template(get_plan_details_resp, self.sample_get_plan_details_resp, 200))
            assert_that(get_plan_details_resp.json()['name'], equal_to(updated_name))
            assert_that(get_plan_details_resp.json()['features'], equal_to(updated_features))

        finally:
            # Delete plan name
            del_plan_resp = resource['prod_md'].del_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(del_plan_resp, 200))

            get_plan_after_delete_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(get_plan_after_delete_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skipif(os.environ.get('ENV') == 'ppd',
                        reason='[SPSS-4673] In PPD delete features API is throwing 400 bad request error')
    def test_24_verify_add_and_remove_feature_in_plan(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        plan_id, name, desc, status, features = resource['prod_md'].create_plan_data()

        # Create plan
        create_plan_resp = resource['prod_md'] \
            .post_create_plan_api(plan_id=plan_id, name=name, desc=desc, status=status, features=features)
        assert_that(self.validate_response_template(create_plan_resp, self.sample_created_plan_resp, 201))
        assert_that(create_plan_resp.json()['planID'], equal_to(plan_id))

        try:
            # Add features in the plan
            updated_features = ['MANAGE_COST_ACCOUNT', 'SHIPPING_RATE', 'VIEW_CONTACTS']
            add_feature_resp = resource['prod_md'].post_add_features_to_plan_api(plan_id=plan_id, features=updated_features)
            assert_that(self.validate_response_code(add_feature_resp, 200))

            new_features = resource['prod_md']\
                .append_elements_from_feature_list(ft_list_1=features, ft_list_2=updated_features)

            get_plan_after_add_ft_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_template(get_plan_after_add_ft_resp, self.sample_get_plan_details_resp, 200))
            assert_that(sorted(get_plan_after_add_ft_resp.json()['features']), equal_to(new_features))

            # Remove features from the plan
            remove_features = ['MANAGE_CONTACTS', 'MANAGE_COST_ACCOUNT']
            del_feature_resp = resource['prod_md'].del_features_from_plan_api(plan_id=plan_id, features=remove_features)
            assert_that(self.validate_response_code(del_feature_resp, 200))

            features_after_remove = resource['prod_md'] \
                .remove_elements_from_feature_list(ft_list_1=features, ft_list_2=remove_features)

            get_plan_after_del_ft_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_template(get_plan_after_del_ft_resp, self.sample_get_plan_details_resp, 200))
            assert_that(sorted(get_plan_after_del_ft_resp.json()['features']), equal_to(features_after_remove))

        finally:
            # Delete plan name
            del_plan_resp = resource['prod_md'].del_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(del_plan_resp, 200))

            get_plan_after_delete_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(get_plan_after_delete_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_25_verify_adding_duplicate_feature_is_not_allowed_in_plan(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        plan_id, name, desc, status, features = resource['prod_md'].create_plan_data()

        # Create plan
        create_plan_resp = resource['prod_md'] \
            .post_create_plan_api(plan_id=plan_id, name=name, desc=desc, status=status, features=features)
        assert_that(self.validate_response_template(create_plan_resp, self.sample_created_plan_resp, 201))
        assert_that(create_plan_resp.json()['planID'], equal_to(plan_id))

        try:
            get_plan_after_add_ft_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_template(get_plan_after_add_ft_resp, self.sample_get_plan_details_resp, 200))
            assert_that(sorted(get_plan_after_add_ft_resp.json()['features']), equal_to(features))

            # Add same features in the plan
            add_feature_resp = resource['prod_md'].post_add_features_to_plan_api(plan_id=plan_id, features=features)
            exp_error_resp = resource['prod_md'].build_exp_error_message_plan_response(plan_id=plan_id, features=features)
            assert_that(self.validate_response_template(add_feature_resp, exp_error_resp, 400))

        finally:
            # Delete plan name
            del_plan_resp = resource['prod_md'].del_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(del_plan_resp, 200))

            get_plan_after_delete_resp = resource['prod_md'].get_plan_by_plan_id_api(plan_id=plan_id)
            assert_that(self.validate_response_code(get_plan_after_delete_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_26_verify_get_role_template_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_role_templates_resp = resource['prod_md'].get_role_templates_from_token_api()
        assert_that(self.compare_response_objects(get_role_templates_resp.json()[0],
                                                  self.sample_get_role_template_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_27_verify_get_role_templates_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_role_templates_count_resp = resource['prod_md'].get_role_templates_count_from_token_api()
        assert_that(self.validate_response_template(get_role_templates_count_resp,
                                                    self.sample_get_role_templates_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_28_verify_get_role_template_details_by_role_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_role_template_details_resp = resource['prod_md']\
            .get_role_template_by_role_id_api(role_id='PITNEYSHIP_ADMIN')
        assert_that(
            self.validate_response_template(get_role_template_details_resp, self.sample_get_role_template_details_resp, 200))
        assert_that(get_role_template_details_resp.json()['roleID'], equal_to('PITNEYSHIP_ADMIN'))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_29_verify_get_role_template_features_by_role_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_role_template_features_resp = resource['prod_md']\
            .get_role_template_features_by_role_id_api(role_id='PITNEYSHIP_ADMIN')
        assert_that(self.compare_response_objects(get_role_template_features_resp.json()[0],
                                                  self.sample_get_plan_feature_resp))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_30_verify_create_update_archive_role_template(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id, name, features = resource['prod_md'].create_role_template_data(archive_plan=True)

        # Create role template
        create_role_template_resp = resource['prod_md'] \
            .post_create_role_template_api(role_id=role_id, name=name, features=features)
        assert_that(self.validate_response_template(create_role_template_resp, self.sample_created_plan_resp, 201))
        assert_that(create_role_template_resp.json()['roleID'], equal_to(role_id))

        try:
            # Update role template name
            updated_name = generate_random_string()
            updated_features = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER', 'VIEW_CONTACTS']
            update_role_template_resp = resource['prod_md'] \
                .put_update_role_template_api(role_id=role_id, name=updated_name, features=updated_features)
            assert_that(self.validate_response_code(update_role_template_resp, 200))

            get_role_template_details_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_template(get_role_template_details_resp,
                                                        self.sample_get_role_template_details_resp, 200))
            assert_that(get_role_template_details_resp.json()['name'], equal_to(updated_name))
            assert_that(get_role_template_details_resp.json()['features'], equal_to(updated_features))

        finally:
            # Archive role template name
            archive_role_template_resp = resource['prod_md'].put_archive_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(archive_role_template_resp, 200))

            get_role_template_after_archive_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(get_role_template_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_31_verify_create_update_delete_role_template(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id, name, features = resource['prod_md'].create_role_template_data()

        # Create role template
        create_role_template_resp = resource['prod_md'] \
            .post_create_role_template_api(role_id=role_id, name=name, features=features)
        assert_that(self.validate_response_template(create_role_template_resp, self.sample_created_plan_resp, 201))
        assert_that(create_role_template_resp.json()['roleID'], equal_to(role_id))

        try:
            # Update role template name
            updated_name = generate_random_string()
            updated_features = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER', 'VIEW_CONTACTS']
            update_role_template_resp = resource['prod_md'] \
                .put_update_role_template_api(role_id=role_id, name=updated_name, features=updated_features)
            assert_that(self.validate_response_code(update_role_template_resp, 200))

            get_role_template_details_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_template(get_role_template_details_resp,
                                                        self.sample_get_role_template_details_resp, 200))
            assert_that(get_role_template_details_resp.json()['name'], equal_to(updated_name))
            assert_that(get_role_template_details_resp.json()['features'], equal_to(updated_features))

        finally:
            # Delete role template name
            del_role_template_resp = resource['prod_md'].del_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(del_role_template_resp, 200))

            get_role_template_after_archive_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(get_role_template_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skipif(os.environ.get('ENV') == 'ppd',
                        reason='[SPSS-4673] In PPD delete features API is throwing 400 bad request error')
    def test_32_verify_add_and_remove_feature_in_role_template(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id, name, features = resource['prod_md'].create_role_template_data()

        # Create role template
        create_role_template_resp = resource['prod_md'] \
            .post_create_role_template_api(role_id=role_id, name=name, features=features)
        assert_that(self.validate_response_template(create_role_template_resp, self.sample_created_plan_resp, 201))
        assert_that(create_role_template_resp.json()['roleID'], equal_to(role_id))

        try:
            # Add features in the role template
            updated_features = ['MANAGE_COST_ACCOUNT', 'SHIPPING_RATE', 'VIEW_CONTACTS']
            add_feature_resp = resource['prod_md'].post_add_features_to_role_template_api(role_id=role_id, features=updated_features)
            assert_that(self.validate_response_code(add_feature_resp, 200))

            new_features = resource['prod_md'] \
                .append_elements_from_feature_list(ft_list_1=features, ft_list_2=updated_features)

            get_role_template_after_add_ft_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_template(get_role_template_after_add_ft_resp,
                                                        self.sample_get_role_template_details_resp, 200))
            assert_that(sorted(get_role_template_after_add_ft_resp.json()['features']), equal_to(new_features))

            # Remove features from the role template
            remove_features = ['MANAGE_CONTACTS', 'MANAGE_COST_ACCOUNT']
            del_feature_resp = resource['prod_md'].del_features_from_role_template_api(role_id=role_id, features=remove_features)
            assert_that(self.validate_response_code(del_feature_resp, 200))

            features_after_remove = resource['prod_md'] \
                .remove_elements_from_feature_list(ft_list_1=features, ft_list_2=remove_features)

            get_role_template_after_del_ft_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_template(get_role_template_after_del_ft_resp,
                                                        self.sample_get_role_template_details_resp, 200))
            assert_that(sorted(get_role_template_after_del_ft_resp.json()['features']), equal_to(features_after_remove))

        finally:
            # Delete role template
            del_role_template_resp = resource['prod_md'].del_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(del_role_template_resp, 200))

            get_role_template_after_delete_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(get_role_template_after_delete_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_33_verify_adding_duplicate_feature_is_not_allowed_in_role_template(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id, name, features = resource['prod_md'].create_role_template_data()

        # Create role template
        create_role_template_resp = resource['prod_md'] \
            .post_create_role_template_api(role_id=role_id, name=name, features=features)
        assert_that(self.validate_response_template(create_role_template_resp, self.sample_created_plan_resp, 201))
        assert_that(create_role_template_resp.json()['roleID'], equal_to(role_id))

        try:
            get_role_template_after_add_ft_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_template(get_role_template_after_add_ft_resp,
                                                        self.sample_get_role_template_details_resp, 200))
            assert_that(sorted(get_role_template_after_add_ft_resp.json()['features']), equal_to(features))

            # Add same features in the role template
            add_feature_resp = resource['prod_md'].post_add_features_to_role_template_api(role_id=role_id, features=features)
            exp_error_resp = resource['prod_md'].build_exp_error_message_role_response(role_id=role_id, features=features)
            assert_that(self.validate_response_template(add_feature_resp, exp_error_resp, 400))

        finally:
            # Delete role template
            del_role_template_resp = resource['prod_md'].del_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(del_role_template_resp, 200))

            get_role_template_after_delete_resp = resource['prod_md'].get_role_template_by_role_id_api(role_id=role_id)
            assert_that(self.validate_response_code(get_role_template_after_delete_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_34_verify_get_admin_roles_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_admin_roles_resp = resource['prod_md'].get_admin_roles_from_token_api()
        assert_that(self.compare_response_objects(get_admin_roles_resp.json()[0],
                                                  self.sample_get_admin_role_details_resp))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    @pytest.mark.parametrize('admin_type, group_name', [('PB_ADMIN', 'idp-spa-admins'),
                                                        ('PB_OPERATOR', 'idp-spa-operators'),
                                                        ('PB_SERVICE', 'idp-spa-svcusers'),
                                                        ('PB_SUPPORT', 'idp-spa-support')])
    def test_35_verify_admin_role_details_by_admin_type_and_group_name(self, resource, admin_type, group_name):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        derived_group_name = resource['prod_md'].derive_group_name(group_name=group_name)
        get_admin_role_details_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=admin_type)
        assert_that(self.validate_response_code(get_admin_role_details_resp, 200))
        assert_that(get_admin_role_details_resp.json()['roleID'], equal_to(admin_type))
        assert_that(get_admin_role_details_resp.json()['oktaGroupName'], equal_to(derived_group_name))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    @pytest.mark.parametrize('admin_type', ['PB_ADMIN', 'PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT'])
    def test_36_verify_admin_role_details_by_okta_group_id(self, resource, admin_type):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        group_id, group_name, features = resource['prod_md'].get_admin_role_details_by_admin_type(admin_type=admin_type)

        get_admin_role_details_resp = resource['prod_md'].get_admin_role_by_group_id_api(group_id=group_id)
        assert_that(
            self.validate_response_template(get_admin_role_details_resp, self.sample_get_admin_role_details_resp, 200))
        assert_that(get_admin_role_details_resp.json()['roleID'], equal_to(admin_type))
        assert_that(get_admin_role_details_resp.json()['oktaGroupID'], equal_to(group_id))
        assert_that(get_admin_role_details_resp.json()['oktaGroupName'], equal_to(group_name))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.parametrize('admin_type, group_name', [('PB_ADMIN', 'idp-spa-admins'),
                                                        ('PB_OPERATOR', 'idp-spa-operators'),
                                                        ('PB_SERVICE', 'idp-spa-svcusers'),
                                                        ('PB_SUPPORT', 'idp-spa-support')])
    def test_37_verify_admin_role_details_by_okta_group_name(self, resource, admin_type, group_name):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        group_name = group_name + '-' + str(self.app_config.env_cfg['env']).lower()

        get_admin_role_details_resp = resource['prod_md'].post_get_admin_roles_by_group_name_api(group_name=group_name)
        assert_that(self.validate_response_code(get_admin_role_details_resp, 200))
        assert_that(get_admin_role_details_resp.json()[0]['roleID'], equal_to(admin_type))
        assert_that(get_admin_role_details_resp.json()[0]['oktaGroupName'], equal_to(group_name))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.parametrize('admin_type', ['PB_ADMIN'])
    def test_38_verify_get_admin_role(self, resource, admin_type):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id, name, group_id, group_name, features = resource['prod_md']\
            .create_admin_role_template_data(admin_type=admin_type)

        # Create admin role
        create_admin_role_resp = resource['prod_md'] \
            .post_create_admin_roles_api(role_id=role_id, name=name, group_id=group_id, group_name=group_name,
                                         features=features)
        assert_that(self.validate_response_template(create_admin_role_resp, self.sample_created_admin_roles_resp, 201))
        assert_that(create_admin_role_resp.json()['roleID'], equal_to(role_id))

        get_admin_role_details_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=role_id)
        assert_that(self.validate_response_template(get_admin_role_details_resp,
                                                    self.sample_get_admin_role_details_resp, 200))
        assert_that(get_admin_role_details_resp.json()['name'], equal_to(name))
        assert_that(sorted(get_admin_role_details_resp.json()['features']), equal_to(sorted(features)))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.skipif(os.environ.get('ENV') == 'ppd',
                        reason='[SPSS-4673] In PPD delete features API is throwing 400 bad request error')
    def test_39_verify_add_and_remove_feature_in_admin_role(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id = resource['prod_md'].get_subs_role_id()

        get_admin_role_details_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=role_id)
        features = sorted(get_admin_role_details_resp.json()['features'])

        # Add features in the admin roles
        updated_features = ['VIEW_CONTACTS']
        add_feature_resp = resource['prod_md'].post_add_features_to_admin_role_api(role_id=role_id, features=updated_features)
        assert_that(self.validate_response_code(add_feature_resp, 200))

        new_features = resource['prod_md']\
            .append_elements_from_feature_list(ft_list_1=features, ft_list_2=updated_features)

        get_admin_role_after_add_ft_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=role_id)
        assert_that(self.validate_response_template(get_admin_role_after_add_ft_resp,
                                                    self.sample_get_admin_role_details_resp, 200))
        assert_that(sorted(get_admin_role_after_add_ft_resp.json()['features']), equal_to(new_features))

        # Remove features from the admin roles
        remove_features = ['VIEW_CONTACTS']
        del_feature_resp = resource['prod_md'].del_features_from_admin_role_api(role_id=role_id, features=remove_features)
        assert_that(self.validate_response_code(del_feature_resp, 200))

        features_after_remove = resource['prod_md'] \
            .remove_elements_from_feature_list(ft_list_1=features, ft_list_2=remove_features)

        get_admin_role_after_del_ft_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=role_id)
        assert_that(self.validate_response_template(get_admin_role_after_del_ft_resp,
                                                    self.sample_get_admin_role_details_resp, 200))
        assert_that(sorted(get_admin_role_after_del_ft_resp.json()['features']), equal_to(features_after_remove))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_40_verify_adding_duplicate_feature_is_not_allowed_in_admin_role(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        role_id = resource['prod_md'].get_subs_role_id()
        get_admin_role_details_resp = resource['prod_md'].get_admin_roles_by_role_id_api(role_id=role_id)
        features = sorted(get_admin_role_details_resp.json()['features'])

        # Add same features in the admin roles
        add_feature_resp = resource['prod_md']\
            .post_add_features_to_admin_role_api(role_id=role_id, features=features)
        exp_error_resp = resource['prod_md'].build_exp_error_message_role_response(role_id=role_id, features=features)
        assert_that(self.validate_response_template(add_feature_resp, exp_error_resp, 400))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_41_verify_get_hubs_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_hubs_resp = resource['prod_md'].get_hubs_from_token_api()
        assert_that(self.compare_response_objects(get_hubs_resp.json()[0], self.sample_get_hub_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_42_verify_get_hubs_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_hubs_count_resp = resource['prod_md'].get_hubs_count_from_token_api()
        assert_that(self.validate_response_template(get_hubs_count_resp, self.sample_get_hubs_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_43_verify_get_hub_details_by_hub_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_hubs_resp = resource['prod_md'].get_hubs_from_token_api()
        hub_id = get_hubs_resp.json()[0]['hubID']

        get_hub_details_resp = resource['prod_md'].get_hub_by_hub_id_api(hub_id=hub_id)
        assert_that(self.validate_response_template(get_hub_details_resp, self.sample_get_hub_details_resp, 200))
        assert_that(get_hub_details_resp.json()['hubID'], equal_to(hub_id))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    def test_44_verify_create_update_archive_hub(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        hub_id, name, market, country = resource['prod_md'].create_hub_data(archive_plan=True)

        # Create hub
        create_hub_resp = resource['prod_md'].post_create_hub_api(hub_id=hub_id, name=name, market=market,
                                                                  country=country)
        assert_that(self.validate_response_template(create_hub_resp, self.sample_created_hub_resp, 201))
        assert_that(create_hub_resp.json()['hubID'], equal_to(hub_id))

        try:
            # Update hub name
            updated_name = generate_random_string(char_count=15)
            update_hub_resp = resource['prod_md'].put_update_hub_api(hub_id=hub_id, name=updated_name, market=market,
                                                                     country=country)
            assert_that(self.validate_response_code(update_hub_resp, 200))

            get_hub_resp = resource['prod_md'].get_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_template(get_hub_resp, self.sample_get_hub_details_resp, 200))
            assert_that(get_hub_resp.json()['name'], equal_to(updated_name))

        finally:
            # Archive hub
            archive_hub_resp = resource['prod_md'].put_archive_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_code(archive_hub_resp, 200))

            get_hub_after_archive_resp = resource['prod_md'].get_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_code(get_hub_after_archive_resp, 404))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_45_verify_create_update_delete_hub(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        hub_id, name, market, country = resource['prod_md'].create_hub_data()

        # Create hub
        create_hub_resp = resource['prod_md'].post_create_hub_api(hub_id=hub_id, name=name, market=market,
                                                                  country=country)
        assert_that(self.validate_response_template(create_hub_resp, self.sample_created_hub_resp, 201))
        assert_that(create_hub_resp.json()['hubID'], equal_to(hub_id))

        try:
            # Update hub name
            updated_name = generate_random_string(char_count=15)
            update_hub_resp = resource['prod_md'].put_update_hub_api(hub_id=hub_id, name=updated_name, market=market,
                                                                     country=country)
            assert_that(self.validate_response_code(update_hub_resp, 200))

            get_hub_resp = resource['prod_md'].get_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_template(get_hub_resp, self.sample_get_hub_details_resp, 200))
            assert_that(get_hub_resp.json()['name'], equal_to(updated_name))

        finally:
            # Delete hub
            del_hub_resp = resource['prod_md'].del_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_code(del_hub_resp, 200))

            get_hub_after_del_resp = resource['prod_md'].get_hub_by_hub_id_api(hub_id=hub_id)
            assert_that(self.validate_response_code(get_hub_after_del_resp, 404))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_46_verify_get_postage_values_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_postage_values_resp = resource['prod_md'].get_postage_values_from_token_api()
        assert_that(self.compare_response_objects(get_postage_values_resp.json()[0],
                                                  self.sample_postage_value_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_47_verify_get_postage_value_details_by_postage_value_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_postage_value_resp = resource['prod_md'].get_postage_values_from_token_api()
        postage_value_id = get_postage_value_resp.json()[0]['postageValueID']

        get_postage_value_details_resp = resource['prod_md']\
            .get_postage_value_by_postage_value_id_api(postage_value_id=postage_value_id)
        assert_that(self.validate_response_template(get_postage_value_details_resp,
                                                    self.sample_postage_value_details_resp, 200))
        assert_that(get_postage_value_details_resp.json()['postageValueID'], equal_to(postage_value_id))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_48_verify_create_postage_value(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        number = str(random.randint(1, 999))
        display_value = 'FCM SPSS Test ' + generate_random_string()
        value = '0.5|LTR|' + number

        # Create postage value
        create_postage_value_resp = resource['prod_md'].post_create_postage_value_api(display_value=display_value, value=value)
        assert_that(self.validate_response_template(create_postage_value_resp, self.sample_created_postage_value_resp, 201))
        postage_value_id = create_postage_value_resp.json()['postageValueID']

        get_postage_value_details_resp = resource['prod_md'] \
            .get_postage_value_by_postage_value_id_api(postage_value_id=postage_value_id)
        assert_that(self.validate_response_template(get_postage_value_details_resp,
                                                    self.sample_postage_value_details_resp, 200))
        assert_that(get_postage_value_details_resp.json()['postageValueID'], equal_to(postage_value_id))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_49_verify_get_integrators_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_integrators_resp = resource['prod_md'].get_integrators_from_token_api()
        assert_that(self.compare_response_objects(get_integrators_resp.json()[0],
                                                  self.sample_integrator_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_47_verify_get_integrator_details_by_integrator_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_integrator_resp = resource['prod_md'].get_integrators_from_token_api()
        integrator_id = get_integrator_resp.json()[0]['integratorID']

        get_integrator_details_resp = resource['prod_md'] \
            .get_integrator_by_integrator_id_api(integrator_id=integrator_id)
        assert_that(self.validate_response_template(get_integrator_details_resp,
                                                    self.sample_integrator_details_resp, 200))
        assert_that(get_integrator_details_resp.json()['integratorID'], equal_to(integrator_id))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_48_verify_create_integrator(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        integrator_id, client_id, name, q_url, notify_flag, notification_q_url = \
            resource['prod_md'].create_integrator_data()

        # Create integrator
        create_integrator_resp = resource['prod_md']\
            .post_create_integrator_api(integrator_id=integrator_id, client_id=client_id, name=name, q_url=q_url,
                                        notify_flag=notify_flag, notification_q_url=notification_q_url)
        assert_that(
            self.validate_response_template(create_integrator_resp, self.sample_integrator_details_resp, 200))
        integrator_id = create_integrator_resp.json()['integratorID']

        get_integrator_details_resp = resource['prod_md'] \
            .get_integrator_by_integrator_id_api(integrator_id=integrator_id)
        assert_that(self.validate_response_template(get_integrator_details_resp,
                                                    self.sample_integrator_details_resp, 200))
        assert_that(get_integrator_details_resp.json()['integratorID'], equal_to(integrator_id))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_49_verify_get_locale_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_locale_resp = resource['prod_md'].get_locales_from_token_api()
        assert_that(self.compare_response_objects(get_locale_resp.json()[0], self.sample_locale_details_resp))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_50_verify_get_locales_count_by_token(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_locales_count_resp = resource['prod_md'].get_locales_count_from_token_api()
        assert_that(self.validate_response_template(get_locales_count_resp, self.sample_get_locales_count_resp, 200))

    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_fedramp_reg
    def test_51_verify_get_locale_details_by_locale_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_locales_resp = resource['prod_md'].get_locales_from_token_api()
        locale_id = get_locales_resp.json()[0]['localeID']

        get_locale_details_resp = resource['prod_md'].get_locale_by_locale_id_api(locale_id=locale_id)
        assert_that(self.validate_response_template(get_locale_details_resp, self.sample_locale_details_resp, 200))
        assert_that(get_locale_details_resp.json()['localeID'], equal_to(locale_id))

    @pytest.mark.product_metadata_sp360commercial
    @pytest.mark.product_metadata_sp360commercial_reg
    @pytest.mark.product_metadata_sp360commercial_smoke
    @pytest.mark.product_metadata_fedramp
    @pytest.mark.product_metadata_fedramp_reg
    @pytest.mark.product_metadata_fedramp_smoke
    @pytest.mark.active_active_ppd
    def test_52_verify_create_update_delete_locale(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        locale_id, country, supported_locales = resource['prod_md'].create_locale_data()

        # Create locale
        create_locale_resp = resource['prod_md'].post_create_locale_api(locale_id=locale_id, country=country,
                                                                        supported_locales=supported_locales)
        assert_that(self.validate_response_template(create_locale_resp, self.sample_created_locale_resp, 201))
        assert_that(create_locale_resp.json()['localeID'], equal_to(locale_id))

        try:
            # Update locale
            updated_supported_locales = ['en_US', 'en_AU']
            update_locale_resp = resource['prod_md'].put_update_locale_api(locale_id=locale_id, country=country,
                                                                           supported_locales=updated_supported_locales)
            assert_that(self.validate_response_code(update_locale_resp, 200))

            get_locale_resp = resource['prod_md'].get_locale_by_locale_id_api(locale_id=locale_id)
            assert_that(self.validate_response_template(get_locale_resp, self.sample_locale_details_resp, 200))
            assert_that(sorted(get_locale_resp.json()['supportedLocales']), equal_to(sorted(updated_supported_locales)))

        finally:
            # Delete locale
            del_hub_resp = resource['prod_md'].del_locale_by_locale_id_api(locale_id=locale_id)
            assert_that(self.validate_response_code(del_hub_resp, 200))

            get_locale_after_del_resp = resource['prod_md'].get_locale_by_locale_id_api(locale_id=locale_id)
            assert_that(self.validate_response_code(get_locale_after_del_resp, 404))
