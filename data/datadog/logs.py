"""
Search logs returns "OK" response
"""
import pandas as pd
import re
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page \
    import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

""" pre-chunk data due to 1000-log response limit """
start = datetime(2022, 10, 12)
end = datetime(2022, 10, 13)
num_days = (end - start).days
periods_per_day = 12  # rough calculation to accommodate all logs
num_periods = num_days*periods_per_day
dates = pd.date_range(start, end, periods=num_periods).tolist()
date_strs = [datetime.strftime(d, '%Y-%m-%dT%H:%M:%S+00:00') for d in dates]

date_pairs = [date_strs[i:i+2] for i in range(len(date_strs) - 2)]

hosts = []
pipettes = []
timestamps = []
volumes = []
channels = []

configuration = Configuration()

channel_map = {
    '8': 8,
    'single': 1
}

with ApiClient(configuration) as api_client:

    for date_pair in date_pairs:

        body = LogsListRequest(
            filter=LogsQueryFilter(
                query="*command.drop_tip*",
                _from=date_pair[0],
                to=date_pair[1],
            ),
            sort=LogsSort.TIMESTAMP_ASCENDING,
            page=LogsListRequestPage(
                limit=1000  # maximum
            ),
        )

        api_instance = LogsApi(api_client)
        response = api_instance.list_logs(body=body)

        for log in response['data']:
            host = log['attributes']['host']
            pipette_matches = re.findall(
                'P(?:\d\d|\d\d\d|\d\d\d\d) .*-Channel GEN.{1}',
                log['attributes']['message'])
            pipette = pipette_matches[0] if len(pipette_matches) > 0 else None
            timestamp = log['attributes']['timestamp']
            volume = float(pipette.split(' ')[0][1:])
            num_channels = channel_map[pipette.split(' ')[1].split('-')[0].lower()]

            hosts.append(host)
            pipettes.append(pipette)
            timestamps.append(timestamp)
            volumes.append(volume)
            channels.append(num_channels)

df_dd = pd.DataFrame(
    {'host': hosts, 'drop-pipette': pipettes, 'timestamp': timestamps,
     'volume': volumes, 'channels': channels})
df_dd_grouped_sum = df_dd.groupby(['host', 'volume']).sum()
print(df_dd_grouped_sum['channels'])
