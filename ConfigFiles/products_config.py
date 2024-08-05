from ConfigFiles.analytics_services import env_config_analytics_services_sp360,env_config_analytics_services_fedramp
from ConfigFiles.devicehub_services import env_config_devicehub, env_config_devicehub_fedramp
from ConfigFiles.ecommerce_services import env_config_ecommerce_sp360, env_config_ecommerce_sp360global
from ConfigFiles.lockers_services import env_config_lockers_services_Sp360 , env_config_lockers_services_Fedramp, \
    env_config_lockers_services_sp360canada, env_config_lockers_services_sp360uk, env_config_lockers_services_sp360global, env_config_lockers_services_govcloud
from ConfigFiles.login_config import login_config_sp360, login_config_sp360canada, login_config_sp360global, \
    login_config_fedramp, login_config_sp360uk, login_config_sp360au , login_config_govcloud
from ConfigFiles.sendtechapps_services import env_config_commercial_cseries, env_config_cseries_sp360global, \
    env_config_commercial_cseries_sp360canada
from ConfigFiles.shared_services import env_config_shared_services_sp360, env_config_shared_services_fedramp, \
    env_config_shared_services_sp360canada, env_config_shared_services_sp360au, env_config_shared_services_sp360global, \
    env_config_shared_services_sp360uk
from ConfigFiles.ssp_services import env_config_ssp_services_sp360, env_config_ssp_services_sp360canada
from ConfigFiles.dataagent_services import env_config_dataagent


class products_config:
    """This class is used to define all the constants like Environment,
       Project Config and login config based on different Products below:
       sp360commercial
       sp360global
       sp360canada
       fedramp
    """
    sp360commercial = {
        'dev':
            {
                'ilp_sp360commercial_smoke': env_config_lockers_services_Sp360.dev_config,
                'ilp_sp360commercial': env_config_lockers_services_Sp360.dev_config,
                'badge_idp_sp360commercial_smoke': env_config_lockers_services_Sp360.dev_config,
                'badge_idp_sp360commercial': env_config_lockers_services_Sp360.dev_config,
                'ilp_lms_sp360commercial_smoke': env_config_lockers_services_Sp360.dev_config,
                'ilp_lms_sp360commercial': env_config_lockers_services_Sp360.dev_config,
                'regressioncheck_lockers': env_config_lockers_services_Sp360.dev_config,
                'emailtest': env_config_lockers_services_Sp360.dev_config,
                'accesslevel': env_config_lockers_services_Sp360.dev_config,
                'sendpro_analytics_api_snowflake_sp360commercial': env_config_analytics_services_sp360.dev_config,
                'device_hub_spong': env_config_devicehub.spong_dev_config,
                'device_hub_sp360': env_config_devicehub.sp360_dev_config,
                'subscription_management_sp360commercial': env_config_shared_services_sp360.dev_config,
                'subscription_management_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'subscription_management_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'subscription_carrier_acct_mgmt_sp360commercial': env_config_shared_services_sp360.dev_config,
                'client_management_sp360commercial': env_config_shared_services_sp360.dev_config,
                'client_management_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'client_management_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'cost_account_management_sp360commercial': env_config_shared_services_sp360.dev_config,
                'cost_account_management_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'cost_account_management_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'address_book_management_sp360commercial': env_config_shared_services_sp360.dev_config,
                'address_book_sp360commercial': env_config_shared_services_sp360.dev_config,
                'address_book_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'address_book_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'product_metadata_sp360commercial': env_config_shared_services_sp360.dev_config,
                'product_metadata_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'product_metadata_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'spss_data_generator': env_config_shared_services_sp360.dev_config,
                'bulk_user_onboarding': env_config_shared_services_sp360.dev_config,
                'login_config': login_config_sp360.dev_logIn_config,
                'enrichtoken_sp360commercial': env_config_shared_services_sp360.dev_config,
                'enrichtoken_sp360commercial_smoke': env_config_shared_services_sp360.dev_config,
                'enrichtoken_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'ccbs_users_reg': env_config_shared_services_sp360.dev_config,
                'self_service_portal_api_sp360commercial': env_config_ssp_services_sp360.dev_config,
                'self_service_portal_api_sp360commercial_smoke': env_config_ssp_services_sp360.dev_config,
                'sending_legacy_service_sp360commercial': env_config_commercial_cseries.dev_config,
                'device_hub_sp360commercial': env_config_devicehub.sp360_dev_config,
                'device_hub_sp360commercial_smoke': env_config_devicehub.sp360_dev_config,
                'device_hub_sp360commercial_reg': env_config_devicehub.sp360_dev_config,
                'device_hub_sp1': env_config_devicehub.sp360_dev_config,
                'ecommerce_services_sp360commercial_smoke': env_config_ecommerce_sp360.dev_config,
                'ecommerce_services_sp360commercial_reg': env_config_ecommerce_sp360.dev_config,
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.dev_config,
                'audit_logging_management_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'jit_provisioning_sp360commercial': env_config_shared_services_sp360.dev_config,
                'jit_provisioning_sp360commercial_reg': env_config_shared_services_sp360.dev_config,
                'jit_provisioning_sp360commercial_smoke': env_config_shared_services_sp360.dev_config

            },
        'qa':
            {
                'ilp_sp360commercial': env_config_lockers_services_Sp360.qa_config,
                'regressioncheck_lockers': env_config_lockers_services_Sp360.qa_config,
                'daylocker': env_config_lockers_services_Sp360.qa_config,
                'emailtest': env_config_lockers_services_Sp360.qa_config,
                'emailSSTO': env_config_lockers_services_Sp360.qa_config,
                'accesslevel': env_config_lockers_services_Sp360.qa_config,
                'ilp_kiosk': env_config_lockers_services_Sp360.qa_config,
                'onboarding': env_config_lockers_services_Sp360.qa_config,
                'badge_idp_sp360commercial': env_config_lockers_services_Sp360.qa_config,
                'ilp_lms_sp360commercial': env_config_lockers_services_Sp360.qa_config,
                'sendpro_analytics_api_snowflake_sp360commercial': env_config_analytics_services_sp360.qa_config,
                'wip': env_config_analytics_services_sp360.qa_config,
                'device_hub_spong': env_config_devicehub.spong_qa_config,
                'device_hub_sp360': env_config_devicehub.sp360_qa_config,
                'device_hub_sp360commercial': env_config_devicehub.sp360_qa_config,
                'device_hub_sp360commercial_smoke': env_config_devicehub.sp360_qa_config,
                'device_hub_sp360commercial_reg': env_config_devicehub.sp360_qa_config,
                'device_hub_sp1': env_config_devicehub.sp360_qa_config,
                'device_hub_hbc_flow': env_config_devicehub.sp360_qa_config,
                'device_hub_print_v2': env_config_devicehub.sp360_qa_config,
                'client_management_sp360commercial': env_config_shared_services_sp360.qa_config,
                'client_management_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'client_management_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'subscription_management_sp360commercial': env_config_shared_services_sp360.qa_config,
                'subscription_management_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'subscription_management_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'subscription_carrier_acct_mgmt_sp360commercial': env_config_shared_services_sp360.qa_config,
                'cost_account_management_sp360commercial': env_config_shared_services_sp360.qa_config,
                'cost_account_management_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'cost_account_management_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'address_book_management_sp360commercial': env_config_shared_services_sp360.qa_config,
                'address_book_sp360commercial': env_config_shared_services_sp360.qa_config,
                'address_book_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'address_book_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'product_metadata_sp360commercial': env_config_shared_services_sp360.qa_config,
                'product_metadata_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'product_metadata_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'spss_data_generator': env_config_shared_services_sp360.qa_config,
                'bulk_user_onboarding': env_config_shared_services_sp360.qa_config,
                'login_config': login_config_sp360.qa_logIn_config,
                'enrichtoken_sp360commercial': env_config_shared_services_sp360.qa_config,
                'enrichtoken_sp360commercial_smoke': env_config_shared_services_sp360.qa_config,
                'enrichtoken_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'ccbs_users_reg': env_config_shared_services_sp360.qa_config,
                'self_service_portal_api_sp360commercial': env_config_ssp_services_sp360.qa_config,
                'self_service_portal_api_sp360commercial_smoke': env_config_ssp_services_sp360.qa_config,
                'notification_sp360commercial': env_config_shared_services_sp360.qa_config,
                'notification_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'dataagent': env_config_dataagent.qa_config,
                'sending_legacy_service_sp360commercial': env_config_commercial_cseries.qa_config,
                'sending_legacy_service_sp360commercial_reg': env_config_commercial_cseries.qa_config,
                'custom_fields_management_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'custom_fields_management_sp360commercial': env_config_shared_services_sp360.qa_config,
                'ecommerce_services_sp360commercial_smoke': env_config_ecommerce_sp360.qa_config,
                'ecommerce_services_sp360commercial_reg': env_config_ecommerce_sp360.qa_config,
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.qa_config,
                'audit_logging_management_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'jit_provisioning_sp360commercial': env_config_shared_services_sp360.qa_config,
                'jit_provisioning_sp360commercial_reg': env_config_shared_services_sp360.qa_config,
                'jit_provisioning_sp360commercial_smoke': env_config_shared_services_sp360.qa_config
            },
        'perf':
            {
                'client_management_sp360commercial': env_config_shared_services_sp360.perf_config,
                'client_management_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'client_management_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'subscription_management_sp360commercial': env_config_shared_services_sp360.perf_config,
                'subscription_management_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'subscription_management_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'create_active_subs_users': env_config_shared_services_sp360.perf_config,
                'create_invited_subs_users': env_config_shared_services_sp360.perf_config,
                'subscription_carrier_acct_mgmt_sp360commercial': env_config_shared_services_sp360.perf_config,
                'cost_account_management_sp360commercial': env_config_shared_services_sp360.perf_config,
                'cost_account_management_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'cost_account_management_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'address_book_management_sp360commercial': env_config_shared_services_sp360.perf_config,
                'address_book_sp360commercial': env_config_shared_services_sp360.perf_config,
                'address_book_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'address_book_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'product_metadata_sp360commercial': env_config_shared_services_sp360.perf_config,
                'product_metadata_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'product_metadata_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'ccbs_users_reg': env_config_shared_services_sp360.perf_config,
                'spss_data_generator': env_config_shared_services_sp360.perf_config,
                'bulk_user_onboarding': env_config_shared_services_sp360.perf_config,
                'login_config': login_config_sp360.perf_logIn_config,
                'enrichtoken_sp360commercial': env_config_shared_services_sp360.perf_config,
                'enrichtoken_sp360commercial_smoke': env_config_shared_services_sp360.perf_config,
                'enrichtoken_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'jit_provisioning_sp360commercial': env_config_shared_services_sp360.perf_config,
                'jit_provisioning_sp360commercial_reg': env_config_shared_services_sp360.perf_config,
                'jit_provisioning_sp360commercial_smoke': env_config_shared_services_sp360.perf_config
            },
        'ppd':
            {
                'daylocker': env_config_lockers_services_Sp360.ppd_config,
                'emailtest': env_config_lockers_services_Sp360.ppd_config,
                'emailSSTO': env_config_lockers_services_Sp360.ppd_config,
                'ilp_sp360commercial': env_config_lockers_services_Sp360.ppd_config,
                'regressioncheck_lockers': env_config_lockers_services_Sp360.ppd_config,
                'accesslevel': env_config_lockers_services_Sp360.ppd_config,
                'client_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'client_management_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'subscription_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'active_active_ppd': env_config_shared_services_sp360.ppd_config,
                'subscription_management_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'subscription_carrier_acct_mgmt_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'cost_account_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'cost_account_management_sp360commercial_smoke': env_config_shared_services_sp360.ppd_config,
                'cost_account_management_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'address_book_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'address_book_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'address_book_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'address_book_sp360commercial_smoke': env_config_shared_services_sp360.ppd_config,
                'product_metadata_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'product_metadata_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'ccbs_users_reg': env_config_shared_services_sp360.ppd_config,
                'spss_data_generator': env_config_shared_services_sp360.ppd_config,
                'bulk_user_onboarding': env_config_shared_services_sp360.ppd_config,
                'login_config': login_config_sp360.ppd_logIn_config,
                'enrichtoken_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'enrichtoken_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'dataagent': env_config_dataagent.ppd_config,
                'custom_fields_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'sendpro_analytics_api_snowflake_sp360commercial': env_config_analytics_services_sp360.ppd_config,
                'wip': env_config_analytics_services_sp360.ppd_config,
                'ecommerce_services_sp360commercial_smoke': env_config_ecommerce_sp360.ppd_config,
                'ecommerce_services_sp360commercial_reg': env_config_ecommerce_sp360.ppd_config,
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.ppd_config,
                'audit_logging_management_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'jit_provisioning_sp360commercial': env_config_shared_services_sp360.ppd_config,
                'jit_provisioning_sp360commercial_reg': env_config_shared_services_sp360.ppd_config,
                'jit_provisioning_sp360commercial_smoke': env_config_shared_services_sp360.ppd_config,
                'sending_legacy_service_sp360commercial': env_config_commercial_cseries.ppd_config,
                'sending_legacy_service_sp360commercial_reg': env_config_commercial_cseries.ppd_config
            },
        'prd':
            {
                'client_management_sp360commercial': env_config_shared_services_sp360.prd_config,
                'subscription_management_sp360commercial': env_config_shared_services_sp360.prd_config,
                'active_active_ppd': env_config_shared_services_sp360.prd_config,
                'subscription_management_sp360commercial_reg': env_config_shared_services_sp360.prd_config,
                'subscription_carrier_acct_mgmt_sp360commercial': env_config_shared_services_sp360.prd_config,
                'cost_account_management_sp360commercial': env_config_shared_services_sp360.prd_config,
                'address_book_management_sp360commercial': env_config_shared_services_sp360.prd_config,
                'address_book_sp360commercial': env_config_shared_services_sp360.prd_config,
                'address_book_sp360commercial_reg': env_config_shared_services_sp360.prd_config,
                'address_book_sp360commercial_smoke': env_config_shared_services_sp360.prd_config,
                'product_metadata_sp360commercial': env_config_shared_services_sp360.prd_config,
                'product_metadata_sp360commercial_reg': env_config_shared_services_sp360.prd_config,
                'ccbs_users_reg': env_config_shared_services_sp360.prd_config,
                'spss_data_generator': env_config_shared_services_sp360.prd_config,
                'bulk_user_onboarding': env_config_shared_services_sp360.prd_config,
                'login_config': login_config_sp360.ppd_logIn_config,
                'enrichtoken_sp360commercial': env_config_shared_services_sp360.prd_config,
                'custom_fields_management_sp360commercial': env_config_shared_services_sp360.prd_config
            }

    }

    sp360global = {
        'dev':
            {
                'ecommerce_services_sp360global': env_config_ecommerce_sp360global.dev_config,
                'login_config': login_config_sp360global.dev_logIn_config

            },
        'qa':
            {
                'ecommerce_services_sp360global': env_config_ecommerce_sp360global.qa_config,
                'login_config': login_config_sp360global.qa_logIn_config,
                'sending_legacy_service_sp360global': env_config_cseries_sp360global.qa_config,
                'sending_legacy_service_sp360global_debug': env_config_cseries_sp360global.qa_config,
            },
        'ppd':
            {
                'ecommerce_services': env_config_ecommerce_sp360global.ppd_config,
                'login_config': login_config_sp360global.ppd_logIn_config,
                'ilp_sp360global_smoke': env_config_lockers_services_sp360global.ppd_config,
                'subscription_management_sp360global': env_config_shared_services_sp360global.ppd_config,
                'subscription_management_sp360global_reg': env_config_shared_services_sp360global.ppd_config,
                'subscription_management_sp360global_smoke': env_config_shared_services_sp360global.ppd_config
            },
        'prd':
            {
                'login_config': login_config_sp360global.prd_logIn_config,
                'subscription_management_sp360global': env_config_shared_services_sp360global.ppd_config,
                'subscription_management_sp360global_reg': env_config_shared_services_sp360global.ppd_config,
                'subscription_management_sp360global_smoke': env_config_shared_services_sp360global.ppd_config
            }

    }

    sp360canada = {
        'dev':
            {
                'ecommerce_services': env_config_ecommerce_sp360global.dev_config,
                'login_config': login_config_sp360canada.dev_logIn_config,
                'self_service_portal_api_sp360canada': env_config_ssp_services_sp360canada.dev_config,
                'self_service_portal_api_sp360canada_smoke': env_config_ssp_services_sp360canada.dev_config

            },
        'qa':
            {
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.qa_config,
                'login_config': login_config_sp360canada.qa_logIn_config,
                'self_service_portal_api_sp360canada': env_config_ssp_services_sp360canada.qa_config,
                'self_service_portal_api_sp360canada_smoke': env_config_ssp_services_sp360canada.qa_config,
                'address_book_sp360canada': env_config_shared_services_sp360canada.qa_config,
                'subscription_management_sp360canada': env_config_shared_services_sp360canada.qa_config,
                'sending_legacy_service_sp360commercial': env_config_commercial_cseries_sp360canada.qa_config,
                'sending_legacy_service_sp360commercial_debug': env_config_commercial_cseries_sp360canada.qa_config
            },
        'ppd':
            {
                'ecommerce_services': env_config_ecommerce_sp360global.ppd_config,
                'login_config': login_config_sp360canada.ppd_logIn_config,
                'ilp_sp360commercial': env_config_lockers_services_sp360canada.ppd_config,
                'regressioncheck_lockers': env_config_lockers_services_sp360canada.ppd_config,
                'subscription_management_sp360canada': env_config_shared_services_sp360canada.ppd_config
            }

    }

    fedramp = {
        'dev':
            {
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.dev_config,
                'sendpro_analytics_api_snowflake_sp360commercial': env_config_analytics_services_sp360.dev_config,
                'login_config': login_config_fedramp.dev_logIn_config,
                'ilp_fedramp_smoke': env_config_lockers_services_Fedramp.dev_config,
                'ilp_lms_fedramp_smoke': env_config_lockers_services_Fedramp.dev_config,
                'device_hub_fedramp': env_config_devicehub_fedramp.dev_config,
                'device_hub_fedramp_smoke': env_config_devicehub_fedramp.dev_config,
                'device_hub_fedramp_reg': env_config_devicehub_fedramp.dev_config,
                'ilp_fedramp': env_config_lockers_services_Fedramp.dev_config,
                'emailtest': env_config_lockers_services_Fedramp.dev_config,
                'regressioncheck_lockers': env_config_lockers_services_Fedramp.dev_config,
                'sendpro_analytics_api_snowflake_fedramp': env_config_analytics_services_fedramp.dev_config,
                'cost_account_management_fedramp': env_config_shared_services_fedramp.dev_config,
                'cost_account_management_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'cost_account_management_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'subscription_management_fedramp': env_config_shared_services_fedramp.dev_config,
                'subscription_management_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'subscription_management_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'client_management_fedramp': env_config_shared_services_fedramp.dev_config,
                'client_management_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'client_management_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'product_metadata_fedramp': env_config_shared_services_fedramp.dev_config,
                'product_metadata_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'product_metadata_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'spss_data_generator': env_config_shared_services_fedramp.dev_config,
                'bulk_user_onboarding': env_config_shared_services_fedramp.dev_config,
                'address_book_fedramp': env_config_shared_services_fedramp.dev_config,
                'address_book_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'address_book_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'enrichtoken_fedramp': env_config_shared_services_fedramp.dev_config,
                'enrichtoken_fedramp_smoke': env_config_shared_services_fedramp.dev_config,
                'enrichtoken_fedramp_reg': env_config_shared_services_fedramp.dev_config,
                'custom_fields_management_fedramp': env_config_shared_services_fedramp.dev_config,
                'custom_fields_management_fedramp_reg': env_config_shared_services_fedramp.dev_config
            },
        'qa':
            {
                'ecommerce_services_sp360commercial': env_config_ecommerce_sp360.qa_config,
                'login_config': login_config_fedramp.qa_logIn_config,
                'ilp_fedramp': env_config_lockers_services_Fedramp.qa_config,
                'ilp_lms_fedramp': env_config_lockers_services_Fedramp.qa_config,
                'emailtest': env_config_lockers_services_Fedramp.qa_config,
                'emailSSTO': env_config_lockers_services_Fedramp.qa_config,
                'device_hub_fedramp': env_config_devicehub_fedramp.qa_config,
                'device_hub_fedramp_smoke': env_config_devicehub_fedramp.qa_config,
                'device_hub_fedramp_reg': env_config_devicehub_fedramp.qa_config,
                'regressioncheck_lockers': env_config_lockers_services_Fedramp.qa_config,
                'sendpro_analytics_api_snowflake_fedramp': env_config_analytics_services_fedramp.qa_config,
                'wip': env_config_analytics_services_fedramp.qa_config,
                'cost_account_management_fedramp': env_config_shared_services_fedramp.qa_config,
                'cost_account_management_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'cost_account_management_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'subscription_management_fedramp': env_config_shared_services_fedramp.qa_config,
                'subscription_management_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'subscription_management_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'spss_data_generator': env_config_shared_services_fedramp.qa_config,
                'bulk_user_onboarding': env_config_shared_services_fedramp.qa_config,
                'client_management_fedramp': env_config_shared_services_fedramp.qa_config,
                'client_management_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'client_management_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'product_metadata_fedramp': env_config_shared_services_fedramp.qa_config,
                'product_metadata_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'product_metadata_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'sendpro_analytics_api_snowflake_sp360commercial': env_config_analytics_services_sp360.qa_config,
                'address_book_fedramp': env_config_shared_services_fedramp.qa_config,
                'address_book_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'address_book_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'enrichtoken_fedramp': env_config_shared_services_fedramp.qa_config,
                'enrichtoken_fedramp_smoke': env_config_shared_services_fedramp.qa_config,
                'enrichtoken_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'custom_fields_management_fedramp_reg': env_config_shared_services_fedramp.qa_config,
                'custom_fields_management_fedramp': env_config_shared_services_fedramp.qa_config,
                'notification_fedramp': env_config_shared_services_fedramp.qa_config,
                'notification_fedramp_reg': env_config_shared_services_fedramp.qa_config,
            },
        'ppd':
            {
                'ecommerce_services': env_config_ecommerce_sp360global.ppd_config,
                'login_config': login_config_fedramp.ppd_logIn_config,
                'ilp_fedramp': env_config_lockers_services_Fedramp.ppd_config,
                'emailtest': env_config_lockers_services_Fedramp.ppd_config,
                'emailSSTO': env_config_lockers_services_Fedramp.ppd_config,
                'regressioncheck_lockers': env_config_lockers_services_Fedramp.ppd_config,
                'cost_account_management_fedramp': env_config_shared_services_fedramp.ppd_config,
                'cost_account_management_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'cost_account_management_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'address_book_fedramp': env_config_shared_services_fedramp.ppd_config,
                'address_book_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'address_book_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'subscription_management_fedramp': env_config_shared_services_fedramp.ppd_config,
                'subscription_management_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'subscription_management_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'spss_data_generator': env_config_shared_services_fedramp.ppd_config,
                'bulk_user_onboarding': env_config_shared_services_fedramp.ppd_config,
                'client_management_fedramp': env_config_shared_services_fedramp.ppd_config,
                'client_management_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'client_management_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'product_metadata_fedramp': env_config_shared_services_fedramp.ppd_config,
                'product_metadata_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'product_metadata_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'enrichtoken_fedramp': env_config_shared_services_fedramp.ppd_config,
                'enrichtoken_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'enrichtoken_fedramp_smoke': env_config_shared_services_fedramp.ppd_config,
                'custom_fields_management_fedramp_reg': env_config_shared_services_fedramp.ppd_config,
                'custom_fields_management_fedramp': env_config_shared_services_fedramp.qa_config,
                'sendpro_analytics_api_snowflake_fedramp': env_config_analytics_services_fedramp.ppd_config

            }

    }

    sp360uk = {
        'dev':
            {
                'login_config': login_config_sp360uk.dev_logIn_config
            },
        'qa':
            {
                'login_config': login_config_sp360uk.qa_logIn_config
            },
        'ppd':
            {
                'login_config': login_config_sp360uk.ppd_logIn_config,
                'ilp_sp360uk_smoke': env_config_lockers_services_sp360uk.ppd_config,
                'subscription_management_sp360uk': env_config_shared_services_sp360uk.ppd_config,
                'subscription_management_sp360uk_reg': env_config_shared_services_sp360uk.ppd_config,
                'subscription_management_sp360uk_smoke': env_config_shared_services_sp360uk.ppd_config
            },
        'prd':
            {
                'login_config': login_config_sp360uk.prd_logIn_config,
                'subscription_management_sp360uk': env_config_shared_services_sp360uk.ppd_config,
                'subscription_management_sp360uk_reg': env_config_shared_services_sp360uk.ppd_config,
                'subscription_management_sp360uk_smoke': env_config_shared_services_sp360uk.ppd_config
            }

    }

    sp360au = {
        'ppd':
            {
                'login_config': login_config_sp360au.ppd_logIn_config,
                'subscription_management_sp360au': env_config_shared_services_sp360au.ppd_config
            }

    }

    govcloud = {
        'ppd':
            {
                'login_config': login_config_govcloud.ppd_logIn_config,
                'ilp_govcloud_smoke': env_config_lockers_services_govcloud.ppd_config,
            }

    }
