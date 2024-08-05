import argparse
import datetime
import inspect
import os
import configparser
import re
import requests
from _pytest.fixtures import fixture
from ConfigFiles.config import Config
from FrameworkUtilities.send_email_by_ses import Generate_Email_SES
import logging
import sys
import pytest
from reportportal_client import RPLogger, RPLogHandler
from urllib3.exceptions import InsecureRequestWarning
import getpass
from platform import python_version
from FrameworkUtilities import Crypt
from FrameworkUtilities.common_utils import common_utils

'''@pytest.fixture(scope="session")
def rp_logger(request):
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if hasattr(request.node.config, 'py_test_service'):
        from pytest_reportportal import RPLogger, RPLogHandler
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
    else:
        import sys
        rp_handler = logging.StreamHandler(sys.stdout)
    rp_handler.setLevel(logging.INFO)
    return logger
'''


@pytest.fixture(scope="session")
def rp_logger(request):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create handler for Report Portal if the service has been
    # configured and started.
    if hasattr(request.node.config, 'py_test_service'):
        # Import Report Portal logger and handler to the test module.
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
        # Add additional handlers if it is necessary
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        rp_handler = logging.StreamHandler(sys.stdout)
    # Set INFO level for Report Portal handler.
    rp_handler.setLevel(logging.INFO)
    return logger


@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    try:
        return request.config.getoption("--email_pytest_report")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


parser = argparse.ArgumentParser()
parser.add_argument("--email_pytest_report",
                    dest="email_pytest_report",
                    help="Email pytest report: Y or N",
                    default="N")


def pytest_terminal_summary(terminalreporter, exitstatus):
    "add additional section in terminal summary reporting."
    if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
        with open('htmlreport.html') as f:
            data = f.read()
            scriptindex = data.index("</script>")
            scriptindex = scriptindex + 10
            summaryindex = data.index("<h2>Summary</h2>")
            resultindex = data.index("<h2>Results</h2>")
            newhtml = ""
            newhtml = newhtml + data[0:scriptindex]
            newhtml = newhtml + data[summaryindex:resultindex]
            newhtml = newhtml + "</body></html>"
        # Initialize the Email_Pytest_Report object
        email_obj = Generate_Email_SES()

        # Send html formatted email body message with pytest report as an attachment
        email_obj.generate_email(data=newhtml)


def pytest_addoption(parser):
    try:
        parser.addini("rp_uuid", 'help', type="pathlist")
        parser.addini("rp_endpoint", 'help', type="pathlist")
        parser.addini("rp_project", 'help', type="pathlist")
        parser.addini("rp_launch", 'help', type="pathlist")
        parser.addoption("--email_pytest_report",
                         dest="email_pytest_report",
                         help="Email pytest report: Y or N",
                         default="N")
        parser.addoption('--no_of_records', action='store', default=10)
        # Adding Addoption for Framework related changes
        parser.addoption('--app_env', action='store', default="dev",
                         help='Environment to run the Test Suite on')
        parser.addoption('--integratorId', action='store', default="spong",
                         help='IntegratorId required to run TestSuite')
        parser.addoption('--project_name', action='store', default="ecommerce_services",
                         help='Project name to run test suite')
        parser.addoption('--username', action='store', default="default",
                         help='username pass from command prompt')
        parser.addoption('--password', action='store', default="default"
                         , help='password pass from command prompt')
        parser.addoption('--product_name', action='store', default="sp360commercial"
                         , help='Product name to run  the Test Suite on')

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


# ----------Adding the conftest.py code for EcommConnector API Suite


@pytest.fixture(scope='session', autouse=True)
def context():
    yield {}


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    print()
    print('run status code:', exitstatus)
    passed_amount = sum(1 for result in session.results.values() if result.passed)
    failed_amount = sum(1 for result in session.results.values() if result.failed)
    total_amount = sum(1 for result in session.results.values() if result.outcome)
    file_path = os.getcwd() + "/reports/pytest_html_report.html"
    # send_email_with_attach(file_path, passed_amount, failed_amount, total_amount)


@pytest.fixture(scope='session', autouse=True)
def get_env(request, custom_logger):
    try:
        env = os.environ['ENV']
        custom_logger.info("Initializing {arg1} environment".format(arg1=os.environ['ENV']))
        return env
    except Exception as e:
        env = request.config.getoption('--app_env')
        custom_logger.info("Initializing {arg1} environment".format(arg1=env))
        return env


@pytest.fixture(scope='session', autouse=True)
def get_project_name(pytestconfig, custom_logger):
    project_name = pytestconfig.getoption('-m')
    custom_logger.info("Executing test suite for project '{arg1}'".format(arg1=project_name))
    return project_name


@pytest.fixture(scope='session', autouse=True)
def get_product_name(request, pytestconfig, custom_logger):
    try:
        product_name = os.environ['GRP_PRODUCT']
        custom_logger.info("Initializing {arg1} environment".format(arg1=product_name))
        return product_name
    except Exception as e:
        product_name = request.config.getoption('--product_name')
        custom_logger.info("Initializing {arg1} environment".format(arg1=product_name))
        return product_name


@pytest.fixture(scope='session', autouse=True)
def get_username(request, custom_logger):
    username = request.config.getoption('--username')
    custom_logger.info("Executing test suite for username - {arg1} ".format(arg1=username))
    return username


@pytest.fixture(scope='session', autouse=True)
def get_password(request, custom_logger):
    password = request.config.getoption('--password')
    custom_logger.info("Executing test Suite for password - {arg1} ".format(arg1=password))
    return password


@pytest.fixture(scope='session', autouse=True)
def get_integrator_id(request, custom_logger, get_product_name):

    try:
        if get_product_name == "sp360commercial":
            return "sp360"
        elif get_product_name == "sp360global":
            return "spog"
        elif get_product_name == "fedramp":
            return "sp360"
        elif get_product_name == "sp360canada":
            return "sp360"
    except Exception as e:
        custom_logger.info("Executing test cases for {arg1} ".format(arg1=request.config.getoption('--integratorId')))
        return request.config.getoption('--integratorId')


@pytest.fixture(scope='session', autouse=True)
def app_config(request, get_env, get_project_name, get_product_name, custom_logger):
    cfg = Config(get_env, get_project_name, get_product_name)
    custom_logger.info("Initializing Config.py file for project {arg1} based on environment "
                       "{arg2}".format(arg1=get_project_name, arg2=get_env, arg3=get_product_name))
    yield cfg


@fixture(scope='session', autouse=True)
def general_config(request, custom_logger):
    custom_logger.info("Initializing Config.txt file based")
    path = os.getcwd() + "/ConfigFiles/ecommerce_services/"
    config = configparser.RawConfigParser()
    config.read(os.path.join(path, "config.txt"))
    yield config


def generate_session_token(app_config, data):
    if app_config.env_cfg.get('env') == 'PRD':
        session_token = "Prod_token"
        return session_token
    else:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        resp = requests.post(app_config.logIn_cfg['okta_log_in_auth_url'], data,
                             headers={"Content-Type": "application/json"}, verify=False)
        json_data = resp.json()
        session_Token = json_data['sessionToken']
        return session_Token


def authorize_user(app_config, session_token):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    headr = {"Authorization": "okta_client_credential"}
    updated_url = app_config.logIn_cfg['okta_preview_auth_url']
    params = {'client_id': app_config.logIn_cfg['client_id'],
              'scope': app_config.logIn_cfg['scope'],
              'response_type': app_config.logIn_cfg['response_type'],
              'redirect_uri': app_config.logIn_cfg['redirect_uri'],
              'nonce': app_config.logIn_cfg['nonce'],
              'state': app_config.logIn_cfg['state'],
              'response_mode': app_config.logIn_cfg['response_mode'],
              'sessionToken': app_config.logIn_cfg['sessionToken'].replace('[tok]', str(session_token))}
    response = requests.get(updated_url, headers=headr, params=params, verify=False)
    return response.content


@fixture(scope='session', autouse=True)
def generate_access_token(get_env, app_config, get_username, get_password, custom_logger):
    if app_config.env_cfg.get('env') == 'PRD':
        okta_token = "prod_admin_token"
        yield okta_token
    else:
        if get_username == 'default':
            username = app_config.env_cfg['username']
            password = app_config.env_cfg['enc_pwd']
            data = '{"username":"' + username + '","password":"' + password + '"}'
            custom_logger.info("Generating access token with user - {arg1}, based on environment {arg2}"
                               .format(arg1=username, arg2=get_env))
        else:
            data = '{"username":"' + get_username + '","password":"' + get_password + '"}'
            custom_logger.info("Generating access token with user - {arg1}, based on environment {arg2}"
                               .format(arg1=get_username, arg2=get_env))

        session_token = generate_session_token(app_config, data)
        html_data = authorize_user(app_config, session_token)
        okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
        yield okta_token


@fixture(scope='session', autouse=True)
def client_token(app_config, custom_logger):
    if app_config.env_cfg.get('env') == 'PRD':
        client_token = "prod_client_token"
        yield client_token
    else:
        username = app_config.env_cfg['CLIENTUSERNAME']
        password = app_config.env_cfg['client_pwd']
        custom_logger.info("Generating access token with client user - {arg1}".format(arg1=username))
        data = '{"username":"' + username + '","password":"' + password + '"}'
        session_token = generate_session_token(app_config, data)
        html_data = authorize_user(app_config, session_token)
        client_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
        yield client_token


@fixture(scope='session', autouse=True)
def custom_logger(logLevel=logging.DEBUG):
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_path = os.path.join(os.getcwd(), 'logs')
    if os.path.exists(log_path) is False:
        try:
            os.makedirs(log_path, exist_ok=True)
        except OSError as error:
            print("Directory can not be created with error message {arg1}".format(arg1=error))

    log_file_name = 'logfile_' + str(datetime.datetime.now()).replace(":", "_") + '.log'
    file_handler = logging.FileHandler(log_path + '/' + log_file_name, mode='a')
    file_handler.setLevel(logLevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%y %I:%M:%S %p')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    yield logger


#
# def pytest_html_report_title(report):
#     """ modifying the title  of html report"""
#     report.title = "ECommConnector API Suite"


''' modifying the table pytest environment'''


@fixture(scope='session', autouse=True)
def configure_html_report_env(request, get_env, get_project_name):
    username = getpass.getuser()
    py_version = python_version()

    # overwriting old parameters with  new parameters
    request.config._metadata = {
        "user_name": username,
        "Python_Version": py_version,
        "Environment": get_env,
        "Project_Name": get_project_name
    }

