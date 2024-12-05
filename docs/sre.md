# Site Reliability Engineer (SRE) Documentation

## Overview

The Site Reliability Engineer focuses on ensuring system reliability, uptime, and performance. This document includes processes for monitoring, incident response, and operational optimization.

### Table of Contents

- [Monitoring and Observability](#monitoring-and-observability)
- [Incident Response](#incident-response)
- [Reliability and Resilience Design](#reliability-and-resilience-design)
- [Automation and Optimization](#automation-and-optimization)

---

# Implemented Incident Report Strategy

An incident report is an extremely important factor that can ensure that teams can effectively manage and mitigate incidents. An **incident** is an unplanned interruption to a service or a reduction in the quality of service. 

The aim of an incident report is to:
- Respond to and identify incidents.
- Minimize their impact across applications.
- Most importantly, restore the normal service of operation as quickly as possible.

## Key Components of an Incident Response Strategy

1. **Clearly Identified Roles within a Team**
2. **Well-Communicated Workflow**
3. **Post-Mortem Analysis**
4. **Implementing Automation and Shooting Guide Where Possible**

## Selected Incident Report Strategy

The incident report strategy that will be followed and was chosen is shown in the diagram below:

<img width="629" alt="Screenshot 2024-12-05 at 10 55 20" src="https://github.com/user-attachments/assets/cdf7317e-6b5d-4ac0-927c-0d3eff56de5b">

The incident response strategy seen above is designed to ensure the efficient management of anomalies and the prompt response to any service disruptions to meet SLA, SLO, and SLI requirements. It involves constant monitoring to track key service levels (SLA, SLO, SLI) and identify anomalies like increased latency, high error rates, or decreased availability. The designed strategy will always be monitoring and there will be alerts set up, as soon as something falls under the threshold expected. Azure Alerts are triggered based on these anomalies and sent to Slack channels, allowing for real-time notification to the response team. Upon receiving an alert, the team determines if the anomaly is a security incident, and if so, appropriate actions are taken. Automated self-healing processes are used where applicable. If incidents cannot be resolved automatically, the ChatOps approach is activated, allowing the team to use Slack for direct interactions with monitoring tools to resolve the issue. Impacted users and stakeholders are kept informed throughout the incident response. Once the incident is resolved, a post-mortem analysis is conducted to identify the root cause and document lessons learned to prevent future incidents. 

The types of alert that will need to be implemented and are seen below:
- **Resource Alerts**: Alerts related to Azure resources such as the database, container registry, and key vault.
- **Database Alerts**: Slow query performance, database connection pool exhaustion, replication lag in distributed databases.
- **Container Registry Alerts**: Issues related to container image retrieval or availability.
- **Key Vault Alerts**: Unauthorized access attempts, latency in retrieving secrets, or depletion of key usage quotas.
- **Application Alerts**: Service downtime, high error rates in APIs, and slow application response times.
- **Security Alerts**: Unauthorized login attempts, unusual data access patterns, and vulnerability detections.
- **Custom Business Logic Alerts**: Breaches in KPIs such as transaction failures or high user drop-off rates.

By categorizing alerts in this way, the team can efficiently monitor and address issues in specific areas of the system, ensuring faster incident response and reducing the likelihood of user impact. The alert system, powered by Azure Monitor, is designed to proactively detect and address issues before users notice them by capturing signals that indicate potential problems. When a defined threshold or condition is breached, Azure Monitor initiates alert rules that monitor resource data, trigger alerts, and activate predefined actions.

The alert process begins with alert rules, which monitor your data and detect signals indicating anomalies in specific resources. If these conditions are met, an alert is triggered. Once triggered, the alert initiates the associated action group and updates the alert state. Action groups are then responsible for notifying relevant team members through channels like voice calls, SMS, emails, or even automated workflows. This ensures that incidents are identified early and handled promptly to minimize the impact on the users.

# Alert Criteria

| **Alert Type**         | **Criteria**                                | **Priority** |
|-------------------------|---------------------------------------------|--------------|
| **Service Downtime**    | Service is unreachable for >1 minute        | Critical     |
| **Unauthorized Access** | Multiple failed logins within 5 minutes     | High         |
| **API Error Rate**      | >5% error rate over 10 minutes              | Medium       |
| **Database Performance**| Query time > 500ms for >10% of queries      | Medium       |
| **Page Load Time**      | Load time drops under 2 sec multiple times  | Low          |


# Incident Response Implementation Strategy

For the incident response implementation strategy, we utilize a suite of Azure-based monitoring tools to ensure efficient detection, management, and mitigation of incidents. These tools are pivotal in maintaining the health, availability, and performance of the **Money404 Bank** application while supporting a proactive incident response.

## Monitoring Tools

The tools mentioned in the monitoring strategy—**Azure Monitor**, **Application Insights**, **Log Analytics Workspace**, and **Azure Workbooks**—serve as the backbone for monitoring system health and availability. These tools:

- Collect metrics across all infrastructure components, such as uptime, system resource usage, and performance metrics.
- Provide detailed telemetry data via Application Insights, ensuring the application remains responsive and stable for end-users.
- Deliver dashboards offering a comprehensive overview of system performance, enabling the team to quickly identify deviations from set thresholds.
- Offer a centralized view of system functionality, allowing proactive detection of potential issues before escalation.

## Slack Integration

Slack integration with Azure Alerts forms a crucial part of the incident response strategy. Through this integration:

- Alerts meeting predefined criteria, such as elevated error rates or prolonged downtime, trigger real-time notifications to appropriate team members.
- Immediate awareness is promoted, enabling faster response and collaboration to resolve incidents effectively.

Together, these tools create a comprehensive incident monitoring and response ecosystem, enabling efficient management of system performance, incident mitigation, and a stable user experience for Money404 Bank’s users.

## Future Improvements

Future enhancements to the monitoring and incident response strategy will focus on:

1. **Automation and Predictive Capabilities**:
   - Integrating machine learning algorithms to predict incidents before they occur using historical performance data and anomaly detection.

2. **Advanced Self-Healing Mechanisms**:
   - Automating common resolutions such as restarting failing services or dynamically reallocating resources during traffic spikes.

3. **Distributed Tracing**:
   - Implementing tools to provide deeper insights into request flows across services, aiding in identifying bottlenecks.

4. **Enhanced ChatOps Workflows**:
   - Adding sophisticated workflows and automation, such as triggering incident resolutions directly through Slack commands.

---

# Alert Implementation Details

### Logic App Integration

A **Logic App**, a cloud-based workflow automation service in Microsoft Azure, was implemented to orchestrate workflows and monitor performance.

### Application Insights and Alerts

To monitor the Logic App, **Azure Application Insights (App Insights)** was used. Three distinct types of alerts were created to test functionality:

1. **Performance Alerts**:
   - Monitor response times to ensure operations remain within expected performance thresholds.

2. **Error Alerts**:
   - Notify of failures or exceptions during execution.

3. **Custom Metric Alerts**:
   - Track specific data points, such as workflow step completions or specific statuses.

These alerts ensure any deviation from expected behavior triggers a notification, enabling proactive troubleshooting.

---

## Slack Integration

To enhance monitoring, the Logic App was integrated with **Slack**, enabling real-time notifications of performance and issues.

### Steps for Integration:

1. **Creating a Slack App**:
   - Registered a new app within the Slack Developer Portal to act as a bridge between the Logic App and Slack.

2. **Generating a Webhook URL**:
   - Created a Webhook within the Slack app configuration. The Webhook acts as an HTTP callback allowing the Logic App to send messages to a Slack channel.

### Securing the Webhook URL

To avoid security vulnerabilities:

- The Webhook URL was **not hardcoded** into the application or deployment scripts.
- Slack’s built-in mechanisms automatically deactivate exposed Webhooks to prevent misuse.

### Secure Storage of Webhook

- The Webhook URL was stored securely as an **environment variable** in **GitHub Actions**.
- During deployment, the Logic App retrieves the Webhook URL from the environment variable, ensuring secure and seamless communication with Slack.

By integrating these tools and best practices, the incident response implementation strategy ensures robust monitoring, efficient incident handling, and improved system reliability for Money404 Bank.



