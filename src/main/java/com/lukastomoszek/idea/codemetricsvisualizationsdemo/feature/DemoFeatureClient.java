/*
 * Copyright (c) 2025 Lukáš Tomoszek
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.lukastomoszek.idea.codemetricsvisualizationsdemo.feature;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class DemoFeatureClient {

    private final Map<String, Boolean> featureFlags = new ConcurrentHashMap<>();

    public DemoFeatureClient() {
        featureFlags.put("new-greeting-format", true);
        featureFlags.put("use-caching-for-data", false);
        featureFlags.put("admin-access-enabled", true);
        featureFlags.put("experimental-logging", true);
    }

    public boolean isFeatureEnabled(String featureName, String userId) {
        if ("user456".equals(userId) && "use-caching-for-data".equals(featureName)) {
            return true;
        }
        return featureFlags.getOrDefault(featureName, false);
    }
}
