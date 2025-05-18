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
