# m365-cis-app-audit
Script to automate the CIS Microsoft 365 Foundations Benchmark application usage audit (5.5 of the CIS Microsoft 365 Foundations Benchmark v2.0)

## 5.5 (L1) Ensure the Application Usage report is reviewed at least weekly
* **Description:**
The Application Usage report includes a usage summary for all Software as a Service 
(SaaS) applications that are integrated with the organization's directory.
**Rationale:**
Review the list of app registrations on a regular basis to look for risky apps that users 
have enabled that could cause data spillage or accidental elevation of privilege. 
Attackers can often get access to data illicitly through third-party SaaS applications.
**Audit:**
To verify the report is being reviewed at least weekly, confirm that the necessary 
procedures are in place and being followed. *

* This script is designed for use in the console and will return a list of applications that deviate from a pre-determined list of trusted baseline applications used in your tenant. Further investigation of unknown applications will need to be investigated within Microsoft Entra. This script may also act as a baseline template and could be built into a more robust script.* 

# Overall Usage
1. Create an Entra application that this script will use for authentication and authorization
2. Use baseline_applications.py, to add/remove/update your list of trusted applications in use by users in your tenant
3. Run script, applications that do not exist in your baseline_applications list will be printed to the console
4. Investigate applications in Entra to determine malicious activity
