import pandas as pd 

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # 1. Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    cleaned_data = data[(data['passenger_count'] > 0)&(data['trip_distance'] > 0)]
    print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: rows with trip_distance equals to zero: {data['trip_distance'].isin([0]).sum()}")
    print(cleaned_data.shape)

    # 2. Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    cleaned_data['lpep_pickup_date'] = pd.to_datetime(cleaned_data['lpep_pickup_datetime']).dt.date

    # 3. Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    cleaned_data.columns = cleaned_data.columns.str.replace(' ','_').str.lower()

    return cleaned_data


@test 
def test_output(output, *args):
# Add three assertions:
# vendor_id is one of the existing values in the column (currently)
# passenger_count is greater than 0
# trip_distance is greater than 0    
    assert output['vendorid'].isin([1,2]).any(), 'VendorID is not in 1 or 2'
    assert (output['passenger_count'].isin([0]).sum() == 0).any(), 'Passenger count has zero value in it'
    assert (output['trip_distance'].isin([0]).sum() == 0).any(), 'Trip distance has zero value in it'
