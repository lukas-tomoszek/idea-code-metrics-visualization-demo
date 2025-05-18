package com.lukastomoszek.idea.codemetricsvisualizationsdemo.service;

import com.lukastomoszek.idea.codemetricsvisualizationsdemo.feature.DemoFeatureClient;
import org.springframework.stereotype.Service;

import java.util.Random;

@Service
public class DemoService {

    private final Random random = new Random();
    private final DemoFeatureClient featureClient;

    public DemoService(DemoFeatureClient featureClient) {
        this.featureClient = featureClient;
    }

    public String getSimpleGreeting(String name) {
        try {
            Thread.sleep(random.nextInt(50) + 10);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "Hello, " + name + "!";
    }

    public String getFancyGreeting(String name) {
        if (featureClient.isFeatureEnabled("experimental-logging", name)) {
            System.out.println("Experimental logging active for fancy greeting user: " + name);
        }
        try {
            Thread.sleep(random.nextInt(100) + 50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "Greetings and Salutations, esteemed " + name + "!!!";
    }

    public String fetchData(String id, boolean useCacheFromController) {
        boolean useDetailedLogs = featureClient.isFeatureEnabled("detailed-fetch-logging", id);

        int sleepTime = useCacheFromController ? random.nextInt(20) + 5 : random.nextInt(200) + 100;
        try {
            Thread.sleep(sleepTime);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        String result = "Data for ID: " + id + (useCacheFromController ? " (from cache)" : " (from source)");
        if (useDetailedLogs) {
            result += " [Detailed logging enabled]";
        }
        return result;
    }

    public String processIncomingData(String data) {
        boolean useAdvancedProcessing = featureClient.isFeatureEnabled("advanced-data-processing", "system");

        int baseSleep = useAdvancedProcessing ? 200 : 150;
        try {
            Thread.sleep(random.nextInt(baseSleep) + 75);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        if (data.contains("error_trigger")) {
            if (featureClient.isFeatureEnabled("suppress-known-errors", "system")) {
                System.out.println("Known error trigger '" + data + "' suppressed by feature flag.");
                return "Processed: " + data.toUpperCase() + " (Error Suppressed)";
            }
            throw new IllegalArgumentException("Simulated processing error for data: " + data);
        }
        return "Processed: " + data.toUpperCase() + (useAdvancedProcessing ? " (Advanced)" : "");
    }

    public String retrieveSystemStatus() {
        try {
            Thread.sleep(random.nextInt(30) + 5);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "System OK";
    }
}
