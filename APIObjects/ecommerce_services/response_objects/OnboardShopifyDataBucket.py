def store_details_data_bucket(test_data):
    store_details = {'storeId': test_data['storeId'],
                     'name': test_data['store_name'],
                     'timezone': test_data['store_time_zone'],
                     'country': test_data['store_country'],
                     'weightUnit': test_data['store_weight_unit'],
                     'pricesIncludeTax': test_data['pricesIncludeTax'],
                     'defaultWarehouseId': test_data['defaultWarehouseId']
                     #                     'dimensionUnit': test_data['dimensionUnit']
                     }

    return {'storesDetails': store_details}


def ware_house_details_data_bucket(test_data):
    ware_house_details = {'id': test_data['warehouse_id'],
                          'name': test_data['warehouse_name'],
                          'avail': test_data['avail']
                          }
    return {'warehouses': ware_house_details}


def address_data_bucket(test_data):
    address_details = {
        'id': test_data['address_id'],
        'type': test_data['address_type'],
        'postcode': test_data['address_postal_code'],
        'address1': test_data['address1'],
        'city': test_data['address_city'],
        'fax': test_data['fax'],
        'website': test_data['website']
    }

    return {'address': address_details}


def country_data_bucket(test_data):
    country_details = {
        'code2': test_data['country_code2'],
        'name': test_data['country_name']
    }
    return {'country': country_details}


def state_data_bucket(test_data):
    state_details = {
        'code': test_data['state_code'],
        'name': test_data['state_name']
    }
    return {'state': state_details}
