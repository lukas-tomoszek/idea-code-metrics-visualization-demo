#  Copyright (c) 2025 Lukáš Tomoszek
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import csv
import datetime
import random
import time

BASE_PACKAGE = "com.lukastomoszek.idea.codemetricsvisualizationsdemo"
NUM_RECORDS = 10000
START_DATE = datetime.datetime(2025, 5, 12)
END_DATE = datetime.datetime(2025, 5, 19)
TOTAL_SECONDS = int((END_DATE - START_DATE).total_seconds())

USER_IDS = [f"user{i:03}" for i in range(1, 201)]
ADMIN_USER_IDS = ["admin001", "admin002", "system"]
ALL_USER_IDS = USER_IDS + ADMIN_USER_IDS

FEATURE_NAMES = [
    "new-greeting-format", "use-caching-for-data", "admin-access-enabled",
    "experimental-logging", "detailed-fetch-logging",
    "advanced-data-processing", "suppress-known-errors"
]

APACHE_PATHS_METHODS = [
    ("GET", "/api/demo/greeting"), ("GET", "/api/demo/data/item{:03d}"),
    ("POST", "/api/demo/process"), ("GET", "/api/demo/admin/status")
]

SERVICE_METHODS = [
    f"{BASE_PACKAGE}.service.DemoService.getSimpleGreeting",
    f"{BASE_PACKAGE}.service.DemoService.getFancyGreeting",
    f"{BASE_PACKAGE}.service.DemoService.fetchData",
    f"{BASE_PACKAGE}.service.DemoService.processIncomingData",
    f"{BASE_PACKAGE}.service.DemoService.retrieveSystemStatus"
]

FEATURE_CLIENT_METHOD_FQN = f"{BASE_PACKAGE}.feature.DemoFeatureClient.isFeatureEnabled"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "CustomClient/1.0"
]
IPS = [f"192.168.1.{random.randint(10, 200)}" for _ in range(50)]

user_features_data = {}


def _add_feature_to_user(user_id, feature_name):
    user_features_data.setdefault(user_id, set()).add(feature_name)


def generate_random_timestamp():
    return START_DATE + datetime.timedelta(seconds=random.randint(0, TOTAL_SECONDS))


def format_apache_timestamp(dt):
    return dt.strftime('%d/%b/%Y:%H:%M:%S %z').replace('UTC', '+0000')


def format_csv_timestamp(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def generate_apache_logs(filename="apache_access.log"):
    with open(filename, 'w') as f:
        for _ in range(NUM_RECORDS):
            timestamp = generate_random_timestamp()
            day_of_week = timestamp.weekday()
            http_method, path_template = random.choices(APACHE_PATHS_METHODS, weights=[0.4, 0.3, 0.2, 0.1], k=1)[0]
            path = path_template.format(random.randint(1, 20)) if "{:03d}" in path_template else path_template
            status, response_time = 200, random.randint(30, 300)

            if path == "/api/demo/process":
                if random.random() < 0.20: status = random.choice([500, 503])
                response_time = random.randint(200, 400) if day_of_week >= 3 else random.randint(100, 200)
            elif path.startswith("/api/demo/data/"):
                response_time = random.randint(80 + (day_of_week * 25), 130 + (day_of_week * 25))
            elif path == "/api/demo/greeting":
                response_time = random.randint(50, 100)
            elif path == "/api/demo/admin/status":
                response_time = random.randint(20, 50)
                if random.random() < 0.1: status = 403

            if random.random() < 0.02:
                path, status, response_time = path + "/nonexistent", 404, random.randint(10, 50)

            ip, user_agent = random.choice(IPS), random.choice(USER_AGENTS)
            bytes_sent = random.randint(50, 5000) if status == 200 else random.randint(50, 500)
            f.write(
                f'{ip} - - [{format_apache_timestamp(timestamp)}] "{http_method} {path} HTTP/1.1" {status} {bytes_sent} "-" "{user_agent}" {response_time}\n')
    print(f"Generated {filename}")


def generate_user_features(filename="user_features.csv"):
    global user_features_data
    user_features_data.clear()

    for user_id in random.sample(USER_IDS, k=int(len(USER_IDS) * 0.5 * 0.75)):
        _add_feature_to_user(user_id, "new-greeting-format")

    potential_cache_users = [uid for uid in USER_IDS if "new-greeting-format" not in user_features_data.get(uid, set())]
    for user_id in random.sample(potential_cache_users, k=max(1, int(len(USER_IDS) * 0.6 * 0.05))):
        _add_feature_to_user(user_id, "use-caching-for-data")

    for user_id in ADMIN_USER_IDS:
        _add_feature_to_user(user_id, "admin-access-enabled")
        if user_id == "system":
            _add_feature_to_user(user_id, "advanced-data-processing")
            _add_feature_to_user(user_id, "suppress-known-errors")

    for user_id in ALL_USER_IDS:
        if random.random() < 0.03: _add_feature_to_user(user_id, "experimental-logging")
        if random.random() < 0.8: _add_feature_to_user(user_id, "detailed-fetch-logging")
        if user_id != "system" and random.random() < 0.85: _add_feature_to_user(user_id, "advanced-data-processing")
        if user_id != "system" and random.random() < 0.99: _add_feature_to_user(user_id, "suppress-known-errors")

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "feature_name"])
        for user_id, features in user_features_data.items():
            for feature in features:
                writer.writerow([user_id, feature])
    print(f"Generated {filename}")


def generate_app_activity_logs(filename="application_activity.csv"):
    if not user_features_data: generate_user_features()

    method_user_sets = {method: set() for method in SERVICE_METHODS}
    for user_id in ALL_USER_IDS:
        for method in SERVICE_METHODS:
            if random.random() < 0.3:  # 30% chance this user uses the method
                method_user_sets[method].add(user_id)

    method_weights = [
        len(method_user_sets[m]) / len(ALL_USER_IDS)
        for m in SERVICE_METHODS
    ]

    all_method_calls = []
    service_call_count = int(NUM_RECORDS * 0.7)
    feature_call_count_per_flag = int(NUM_RECORDS * 0.3 / len(FEATURE_NAMES)) if FEATURE_NAMES else 0

    for _ in range(service_call_count):
        timestamp = generate_random_timestamp()
        method_fqn = random.choices(SERVICE_METHODS, weights=method_weights, k=1)[0]
        if method_fqn.endswith("retrieveSystemStatus"):
            user_id = random.choice(ADMIN_USER_IDS)
        else:
            eligible_users = list(method_user_sets[method_fqn])
            user_id = random.choice(eligible_users or ALL_USER_IDS)
        all_method_calls.append({
            'timestamp': timestamp,
            'method_fqn': method_fqn,
            'user_id': user_id,
            'feature_name': None
        })

    for feature_name_to_check in FEATURE_NAMES:
        for _ in range(feature_call_count_per_flag):
            timestamp = generate_random_timestamp()
            user_id = random.choice(ALL_USER_IDS)
            all_method_calls.append({
                'timestamp': timestamp,
                'method_fqn': FEATURE_CLIENT_METHOD_FQN,
                'user_id': user_id,
                'feature_name': feature_name_to_check
            })

    all_method_calls.sort(key=lambda x: x['timestamp'])

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "method_fqn", "user_id", "feature_name"])
        for call in all_method_calls:
            writer.writerow([format_csv_timestamp(call['timestamp']), call['method_fqn'], call['user_id'],
                             call['feature_name'] or ''])
    print(f"Generated {filename}")


if __name__ == "__main__":
    start_time = time.time()
    generate_apache_logs()
    generate_user_features()
    generate_app_activity_logs()
    end_time = time.time()
    print(f"Log generation finished in {end_time - start_time:.2f} seconds.")
