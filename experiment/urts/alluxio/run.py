import os, shutil, time
cur_path = os.getcwd()
project_url = "https://github.com/Alluxio/alluxio.git"
project_root_path = os.path.join(cur_path, "alluxio")
project_module_name = "core"
project_module_path = os.path.join(project_root_path, project_module_name)
module_pom_file_path = os.path.join(project_module_path, "pom.xml")
api_file1_path = os.path.join(project_module_path, "common/src/main/java/alluxio/conf/AlluxioProperties.java")
api_file2_path = os.path.join(project_module_path, "common/src/main/java/alluxio/conf/InstancedConfiguration.java")
api_file3_path = os.path.join(project_module_path, "common/src/main/java/alluxio/conf/path/SpecificPathConfiguration.java")
api_pom_file_path = os.path.join(project_module_path, "pom.xml")
test_copied_path = os.path.join(project_module_path, "common/src/test/java/alluxio")
time_file_path = os.path.join(cur_path, "time.txt")
test_class_num_file_path = os.path.join(cur_path, "test_class_num.txt")
mvn_cmd = "mvn urts:urts -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true -DfailIfNoTests=false | tee out.txt"
mvn_cmd_exclude = "mvn urts:urts -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true -DfailIfNoTests=false | tee out.txt"
commits = ["6f2b2fa59fa5331942048f8e5e8a3a3a831f80b9","5cf33595cb8c6e6d2738a211e12d445b5e98b663","5063016989da5284e1a94e80b7b2f2258aadaa7e","e9136cfd354d28ca9e953b282f4c327a0362d587","e697da0a75d6f98f31d6cdd0c7190bf29d5da827","d3b045247ae9baecc6fe45af8d410df38335d43d","984251fe3345659541c4b2330d2185320fa27738","f64540541748ba088eafbbac37fbd8c0458c410e","3c0275f4b81af80f98c8e0f1043bab8c8803f07c","696cb89bfc8b7dd41393e3003307947d2110e21f","ed7588da4adabc0555a018140b82f2f8215fe506","4c8b555920da6a844f3f30cc70493b563178518d","3064609e7489ea3c2111fd6d3c85b48270dc18f8","a16bc958dd283dc9bc7c9fe7f17627ace327eb28","dc922657fdbb6c5ccbbf2e0c1d2e02c66c921204","278b9e263842d61d7168cc29cac44666bfeea0d0","fa54b1bcd9fc891413cbd168862706d0fad0ad02","067e9d432166d44a82fb26aa1ffa8660b665e2f0","0dfa1615292a5c1adca7023a5f1330110df82482","2df1da2d4f6caa47574640bf54c52447e8c0f3ea","03f686a42238c9e5868132052810f3b5f93be918","38f110d924e016eff159ac1c8bb5cac14d3a2696","ebc291ff23f8b4ab6809a6876283e23287b1c64d","b9c66ca164d363bed9bcefb776a0b0f438d96441","050882ecee4ae4dc1bcf3eadcf0ecab3ca192f53","c6e5c2c1243bb9b07ff013ccc9efbb4146b3c92c","f950a7229e1183fdf5142ba4de6c6c9d9de1b3f6","f4f80a2d571903dbbbd824bf8fc5290a9b1a8d8c","c81d35f48521dcc7bf717594531dc7f76795b9cb","6f3fe6f4637261044b3938e620ac00e6e6e75708","b8aad79c004719566d679632026adefdcba8dea7","efe8f4c3f050910179f480896b424c93990a6941","931a9c136865968584ce9efbed6996d0ffbb601b","534e7d47e83f884469991a2c4b96078f3e24a183","e3af125d920b6aaca3af01fac9db1814f49d0262","62a58635bbd20148e2106c39a05208fd69f06dfb","cf83cc15bd6fd7190d3dc049c1cc619b2ae30a1e","6accf76ff7915a94e78c88d8e0f96a0951d379eb","2d939de0cafdb31f5cc19d3170751cc3fa15a972","061519fcbe25d0b3fbed05c91e2e8acf33ef9eb7","67288abbec68128272de74500b989dd82a24b2fb","5c2619a67c840a82ecaee38ff2d3666b9277cd70","b026dc935573c7fd813d36e585f357bc5bbe8754","fb8965dcd327bdbc9a13ad1281e0297fd4ef1bd4","e3e262816e1654960dcb5fc3877cfd05badd6bb9","a9548650a030d6f87a318f949d187a3e6d722896","f69a6f245b0e5d4ea40d929bcfb35fb805c3f7e6","5de0620f9d01c8c1d06d600428470a4ff69c8b9a","7fc1af3a995002146ef33f83b9c17ce6b9fa2af3","8e38ed90c2910febbf80dfc652993c8e9f313c89"]
configuration_file = ["core-default.properties", "prod1.properties", "prod2.properties"]
component_list = ["common", "client/fs", "client/hdfs", "server/common", "server/proxy", "server/worker"]

# Clone testing project
def clone():
    if os.path.exists(project_root_path):
        shutil.rmtree(project_root_path)
    clone_cmd = "git clone " + project_url
    os.system(clone_cmd)


# Record the experiment time
def record_time(elapsed_time, curConfig, curCommit):
    with open(time_file_path, 'a') as f:
        f.write("{}-{} : {}s\n".format(curConfig, curCommit, elapsed_time))


def record_test_class_number(curConfig, curCommit):
    total_num = 0
    for component in component_list:
        component_path = os.path.join(project_module_path, component) 
        os.chdir(component_path)
        p = os.popen("grep 'Tests ' out.txt | sed -e 's/^.*Tests //' -e 's/.\[0;1;32m//' -e 's/.\[m//' -e 's/.\[1m//' -e 's/.\[0;1m//g' -e 's/.\[m//g' | sed -n 's/run: \([1-9][0-9]*\),.*- in \(.*\)/\2     \1/p' | wc -l")
        total_num += int(p.read())
    with open(test_class_num_file_path, 'a') as f:
        f.write("{}-{} : {}\n".format(curConfig, curCommit, total_num))
    os.chdir(cur_path)


# Modify Get/Set API
def modify_api():
    lines = []
    with open(api_file1_path, 'r') as f:
        for line in f:
            lines.append(line)
    
    with open(api_file1_path, 'w') as f:
        inGet = False
        for line in lines:
            if "import org.slf4j.LoggerFactory;" in line:
                f.write(line)
                f.write("import org.urts.configAware.ConfigListener; // UNIFY_TEST\n")  
                f.write("import alluxio.util.ConfigurationUtils; // UNIFY_TEST\n")
                f.write("import java.lang.management.ManagementFactory; // UNIFY_TEST\n")
            elif "public class AlluxioProperties {" in line:
                f.write(line)
                f.write("  public static String CTEST_FILEPATH = System.getProperty(\"user.dir\").split(\"/alluxio/core/\")[0] + \"/alluxio/core/alluxio-ctest-\" + ManagementFactory.getRuntimeMXBean().getName().split(\"@\")[0] + \".properties\"; // UNIFY_TESTS\n")
            elif "public AlluxioProperties()" in line:
                f.write("  public AlluxioProperties() {\n")
                f.write("    Properties ctestProps = ConfigurationUtils.loadPropertiesFromFile(CTEST_FILEPATH); // UNIFY_TESTS\n")
                f.write("    this.merge2(ctestProps, Source.siteProperty(CTEST_FILEPATH));\n  }\n")
            elif "public AlluxioProperties(AlluxioProperties alluxioProperties) {" in line:
                f.write(line)
                f.write("    Properties ctestProps = ConfigurationUtils.loadPropertiesFromFile(CTEST_FILEPATH); // UNIFY_TESTS\n")
                f.write("    alluxioProperties.merge2(ctestProps, Source.siteProperty(CTEST_FILEPATH)); // UNIFY_TESTS\n")
            elif "public String get(PropertyKey key) {" in line:
                f.write(line)
                inGet = True
            elif inGet:
                if "if (mUserProps.containsKey(key)) {" in line:
                    f.write(line)
                    f.write("ConfigListener.recordGetConfig(key.getName(), mUserProps.get(key).orElse(null)); //UNIFY_TESTS\n")
                elif "return PropertyKey.fromString(key.toString()).getDefaultValue();" in line:
                    f.write("ConfigListener.recordGetConfig(key.getName(), PropertyKey.fromString(key.toString()).getDefaultValue()); //UNIFY_TESTS\n")
                    f.write(line)
                    inGet = False
                else:
                    f.write(line)
            
            elif "public void put(PropertyKey key, String value, Source source) {" in line:
                f.write("  public void put_purged(PropertyKey key, String value, Source source) {\n")
                f.write("    if (!mUserProps.containsKey(key) || source.compareTo(getSource(key)) >= 0) {\n")
                f.write("      mUserProps.put(key, Optional.ofNullable(value));\n")
                f.write("      mSources.put(key, source);\n")
                f.write("      mHash.markOutdated();\n")
                f.write("    }\n")
                f.write("  }\n\n")
                f.write(line)
            
            elif "if (!mUserProps.containsKey(key) || source.compareTo(getSource(key)) >= 0) {" in line:
                f.write(line)
                f.write("      ConfigListener.recordSetConfig(key.getName(), value); //UNIFY_TESTS\n")
            elif "public void merge(Map<?, ?> properties, Source source) {" in line:
                f.write("  public void merge2(Map<?, ?> properties, Source source) {\n")
                f.write("    if (properties == null || properties.isEmpty()) {return;}\n")
                f.write("    for (Map.Entry<?, ?> entry : properties.entrySet()) {\n")
                f.write("      String key = entry.getKey().toString().trim();\n")
                f.write("      String value = entry.getValue() == null ? null : entry.getValue().toString().trim();\n")
                f.write("      PropertyKey propertyKey;\n")
                f.write("      if (PropertyKey.isValid(key)) {propertyKey = PropertyKey.fromString(key);} \n")
                f.write("      else {\n")
                f.write("        LOG.debug(\"Property {} from source {} is unrecognized\", key, source);\n")
                f.write("        propertyKey = PropertyKey.getOrBuildCustom(key);\n")
                f.write("      }\n")
                f.write("      put_purged(propertyKey, value, source);\n")
                f.write("    }\n")
                f.write("    mHash.markOutdated();\n  }\n")
                f.write(line)
            else:
                f.write(line)
        
    lines = []
    with open(api_file2_path, 'r') as f:
        for line in f:
            lines.append(line)
            
    with open(api_file2_path, 'w') as f:
        for line in lines:
            if "import org.slf4j.LoggerFactory;" in line:
                f.write(line)
                f.write("import org.urts.configAware.ConfigListener; // UNIFY_TEST\n")
            elif "return get(key, ConfigurationValueOptions.defaults());" in line:
                f.write("    String propertyValue = get(key, ConfigurationValueOptions.defaults()); //UNIFY_TESTS\n")
                f.write("    ConfigListener.recordGetConfig(key.getName(), propertyValue); //UNIFY_TESTS\n")
                f.write("    return propertyValue;\n")
            elif "return value;" in line:
                f.write("    ConfigListener.recordGetConfig(key.getName(), value); //UNIFY_TESTS\n")
                f.write(line)            
            else:
                f.write(line)
    
    lines = []
    with open(api_file3_path, 'r') as f:
        for line in f:
            lines.append(line)
    
    with open(api_file3_path, 'w') as f:
        for line in lines:
            if "          config -> properties.put(key, config.get(key), Source.PATH_DEFAULT));" in line:
                f.write("          config -> properties.put_purged(key, config.get(key), Source.PATH_DEFAULT));\n")
            else:
                f.write(line)


# Add uRTS to pom file
def modify_pom():
    lines = []
    with open(module_pom_file_path, "r") as f:
        for line in f:
            lines.append(line)
    
    with open(module_pom_file_path, "w") as f:
        for line in lines:
            if "</properties>" in line:
                f.write(line)
                insertDepBuild = " \
                            <dependencies>\n \
                                <dependency>\n \
                                <groupId>org.urts</groupId>\n \
                                <artifactId>org.urts.core</artifactId>\n \
                                <version>1.0.0-SNAPSHOT</version>\n \
                                <scope>compile</scope>\n \
                                </dependency>\n \
                            </dependencies>\n \
                            <build>\n \
                                <plugins>\n \
                                <plugin>\n \
                                    <groupId>org.urts</groupId>\n \
                                    <artifactId>urts-maven-plugin</artifactId>\n \
                                    <version>1.0.0-SNAPSHOT</version>\n \
                                </plugin>\n \
                                </plugins>\n \
                            </build>\n "
                f.write(insertDepBuild)
            else:
                f.write(line)



# Run tests
def run_urts(config_file, curConfig, curCommit):
    os.chdir(project_module_path)
    shutil.copy(config_file, "curConfigFile.properties")
    print("=================[uRTS: RUN TestGetConfigValueForConfigAware]=================", flush=True)
    start1 = time.time()
    os.system("mvn surefire:test -Dtest=TestGetConfigValueForConfigAware -pl common/ -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true")
    end1 = time.time()
    print("=================[uRTS: RUN uRTS]=================", flush=True)
    start2 = time.time()
    for component in component_list:
        print("===============[uRTS: Evaluation: In Component: " + component + " ]===============", flush=True)
        component_path = os.path.join(project_module_path, component)   
        os.chdir(component_path)
        if component == "client/fs":
            os.system(mvn_cmd_exclude)
        else:
            os.system(mvn_cmd)
    end2 = time.time()
    record_time(end1-start1+end2-start2, curConfig, curCommit)
    os.chdir(cur_path)


# Install dependency module
def maven_install_module():
    os.chdir(project_root_path)
    os.system("mvn install -pl core -amd -DskipTests -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true")
    os.chdir(project_module_path)
    os.system("mvn install -am -DskipTests -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true")
    os.chdir(cur_path)


# Prepare config file
def copy_production_config_file(replaced_config_file_path, original_config_file_path):
    shutil.copy(replaced_config_file_path, original_config_file_path)


# Prepare uRTS config file
def prepare_urtsrc_config_file(config_name):
    for component in component_list:
        if component in ["common", "transport"]:
            source_path = os.path.join(cur_path, ".oneurtsrc-" + config_name)
        else:
            source_path = os.path.join(cur_path, ".twourtsrc-" + config_name)
        target_path = os.path.join(project_module_path, component, ".urtsrc")
        shutil.copy(source_path, target_path)


# Checkout to certain version
def checkout_commit(commit):
    os.chdir(project_root_path)
    os.system("git checkout -f " + commit)
    os.chdir(cur_path)


# Prepare test that used to get config values
def copy_get_config_value_test():
    print(test_copied_path)
    source_path = os.path.join(cur_path, "TestGetConfigValueForConfigAware.java")
    target_path = os.path.join(test_copied_path, "TestGetConfigValueForConfigAware.java")
    shutil.copy(source_path, target_path)


# Prepare mapping
def copy_ctest_mapping():
    source_path = os.path.join(cur_path, "mapping")
    target_path = os.path.join(project_module_path, "mapping")
    shutil.copy(source_path, target_path)


# Do not skip Tests in Alluxio
def notSkipTestsInAlluxio():
    pom_file_path = os.path.join(project_root_path, "pom.xml")
    lines = []
    with open(pom_file_path, 'r') as f:
        for line in f:
            lines.append(line)
    
    with open(pom_file_path, 'w') as f:
        for line in lines:
            if "<skipTests>true</skipTests>" in line:
                continue
            else:
                f.write(line)


# Prepare environment and all files
def do_preparation(commit):
    checkout_commit(commit)
    modify_pom()
    notSkipTestsInAlluxio()
    modify_api()
    copy_ctest_mapping()
    copy_get_config_value_test()
    maven_install_module()


def run():
    clone()
    for i in range(len(commits)):
        curCommit = commits[i]
        do_preparation(curCommit)
        for curConfig in configuration_file:
            cur_config_name = curConfig.split(".")[0]
            config_file_name = curConfig + "-" + curCommit
            print("===============[uRTS: Evaluation: " + curCommit + " Config: " + cur_config_name + " ]===============", flush=True)
            replacedConfigFilePath = os.path.join(cur_path, "../../config_files/alluxio/", config_file_name)
            targetConfigFilePath = os.path.join(project_module_path, curConfig)
            if not os.path.exists(replacedConfigFilePath):
                ValueError("Does not have configuration file: " + replacedConfigFilePath)
            copy_production_config_file(replacedConfigFilePath, targetConfigFilePath)
            prepare_urtsrc_config_file(cur_config_name)
            run_urts(replacedConfigFilePath, curConfig, curCommit)
            record_test_class_number(curConfig, curCommit)


if __name__ == '__main__':
    run()
