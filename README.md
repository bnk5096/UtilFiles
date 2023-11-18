# ReadMe

### Directory Organization
- src: The code used for data collection and analysis
- complexity_data: The complexity measurements collected from SonarQube and Metrix++
- static_file_lists: snapshot lists of the files from each repository
- prevalence_vulnerability_data: The data from investigating the odds ratios for vulnerability presence in util files. These files contain exclusion notices. These refer to aliases that fall outside of the source code definitions set by the Vulnerability History Project.

### Files to Remove for Metrix++
- Metrix++ fails entirely on what it considers to be malformed data. The following files were removed from the repositories for the Metrix++ process.
- From struts we exclude:
  -  ./.mvn/wrapper/MavenWrapperDownloader.java
- From httpd
  - ./modules/aaa/mod_auth_digest.c
  - ./modules/metadata/mod_version.c
