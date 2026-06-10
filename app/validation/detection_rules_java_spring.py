JAVA_FILES = [
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
]

SPRING_DEPENDENCIES = [
    "spring-boot-starter",
    "spring-boot-maven-plugin",
    "spring-boot-starter-parent",
]

SQL_DEPENDENCIES = [
    "spring-boot-starter-data-jpa",
    "spring-boot-starter-jdbc",
    "hibernate-core",
    "jooq",
]

NOSQL_DEPENDENCIES = [
    "spring-boot-starter-data-mongodb",
    "spring-boot-starter-data-redis",
    "spring-boot-starter-data-cassandra",
]

DATABASE_PROVIDERS = {
    "postgresql": [
        "org.postgresql",
        "postgresql",
    ],
    "oracle": [
        "com.oracle.database",
        "ojdbc",
    ],
    "mysql": [
        "com.mysql",
        "mysql-connector",
    ],
    "sql-server": [
        "com.microsoft.sqlserver",
        "mssql-jdbc",
    ],
}

TEST_DEPENDENCIES = [
    "spring-boot-starter-test",
    "junit-jupiter",
    "junit",
]