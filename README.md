# ReadMe

### Directory Organization
- src: The code used for data collection and analysis
- complexity_data: The complexity measurements collected from SonarQube and Metrix++
- static_file_lists: snapshot lists of the files from all used repositories other than Linux and Chromium which are too large
- prevalence_vulnerability_data: The data from investigating the odds ratios for vulnerability presence in util files. These files contain exclusion notices. These refer to aliases that fall outside of the source code definitions set by the Vulnerability History Project.

### Files to Remove for Metrix++
- Metrix++ fails entirely on what it considers to be malformed data. The following files were removed from the repositories for the Metrix++ process.
- From struts we exclude:
  -  ./.mvn/wrapper/MavenWrapperDownloader.java
- From httpd
  - ./modules/aaa/mod_auth_digest.c
  - ./modules/metadata/mod_version.c

### SonarQube
- The code as provided assumes that SonarQube is being hosted locally with credentials configured as username: admin and password: password with the project called "test".
- The project token must be configured for proper transfer of data from Sonar Scanner to SonarQube.

### Intended Flow
- Clone each repostory to analyze
- Run odds_ratios.py and odds_ratios_no_renames.py
- Run complexity_manager.py
- Run complexity_data.py