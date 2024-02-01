# m365-cis-app-audit
Script to automate the CIS Microsoft 365 Foundations Benchmark application usage audit (5.5 of the CIS Microsoft 365 Foundations Benchmark v2.0). Description of audit here:

### 5.5 (L1) Ensure the Application Usage report is reviewed at least weekly
- **Description:**
The Application Usage report includes a usage summary for all Software as a Service 
(SaaS) applications that are integrated with the organization's directory.
- **Rationale:**
Review the list of app registrations on a regular basis to look for risky apps that users 
have enabled that could cause data spillage or accidental elevation of privilege. 
Attackers can often get access to data illicitly through third-party SaaS applications.
- **Audit:**
To verify the report is being reviewed at least weekly, confirm that the necessary 
procedures are in place and being followed.

This script is designed for use in the console and will return a list of applications that deviate from a pre-determined list of trusted baseline applications used in your tenant. Further investigation of unknown applications will need to be investigated within Microsoft Entra. This script may also act as a baseline template and could be built into a more robust script.

# Overall Usage
1. Create an Entra application that this script will use for authentication and authorization
2. Use baseline_applications.py, to add/remove/update your list of trusted applications in use by users in your tenant
3. Run script, applications that do not exist in your baseline_applications list will be printed to the console
4. Investigate applications in Entra to determine malicious activity

## Entra Application Creation, Authentication, and Permissions:
### Creation
- To interact with Entra using Python (or any other programing language), you first need to create your own application, assign it permissions, and upload certificates for authentication.
1. Navigate to "entra.microsoft.com" > "Applications" > "Enterprise applications"
2. Select "New application" > "Create your own application"
3. Name your application and leave the default "Non-gallery" option
4. When the application has been created, navigate to "App registrations" in the navigation blade, and find/select your application
5. In "Overview", copy the "Client Id" and "Tenant Id" values for use in the script
### Authentication 
6. Navigate to "Certificates & secrets" > "Certificates" > "Upload certificate"
7. Upload your certificate (see steps below for creation), and copy the "Thumbprint" value to use in the script
### Authorization
8. Navigate to "API permissions" > "Add a permission" > "Microsoft Graph" > "Application permissions"
9. Scroll down to find "Reports" and select "Reports.Read.All"
10. As this is an elevated permission, select "Grant admin consent" on the main API Permissions page.
 

## Certificate Creation
Using openssl, a .key and .cer file need to be generated for client authentication 
Commands:
1. openssl genrsa -out <key_name>.key 2048
2. openssl req -new -key <your_key_name>.key -out <your_csr_name>.csr
3. openssl x509 -req -in <csr_file_name>.csr -signkey <your_key_name>.key -out <your_certificate_name>.crt -days 180
