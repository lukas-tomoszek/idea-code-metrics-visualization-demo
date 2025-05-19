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

package com.lukastomoszek.idea.codemetricsvisualizationsdemo.controller;


import com.lukastomoszek.idea.codemetricsvisualizationsdemo.feature.DemoFeatureClient;
import com.lukastomoszek.idea.codemetricsvisualizationsdemo.service.DemoService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/demo")
public class DemoController {

    private final DemoService demoService;
    private final DemoFeatureClient featureClient;

    public DemoController(DemoService demoService, DemoFeatureClient featureClient) {
        this.demoService = demoService;
        this.featureClient = featureClient;
    }

    @GetMapping("/greeting")
    public String getGreeting(@RequestParam(defaultValue = "World") String name) {
        if (featureClient.isFeatureEnabled("new-greeting-format", "user123")) {
            return demoService.getFancyGreeting(name);
        }
        return demoService.getSimpleGreeting(name);
    }

    @GetMapping("/data/{id}")
    public String getDataById(@PathVariable String id) {
        boolean useCache = featureClient.isFeatureEnabled("use-caching-for-data", "user456");
        return demoService.fetchData(id, useCache);
    }

    @PostMapping("/process")
    public String processData(@RequestBody String data) {
        return demoService.processIncomingData(data);
    }

    @GetMapping("/admin/status")
    public String getAdminStatus() {
        if (!featureClient.isFeatureEnabled("admin-access-enabled", "adminUser")) {
            return "Access Denied";
        }
        return demoService.retrieveSystemStatus();
    }
}
