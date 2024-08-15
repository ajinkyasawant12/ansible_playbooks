#!/bin/bash

#!/bin/bash

# Variables for Find and Replace
SNAPSHOT_SEARCH="SNAPSHOT"
SNAPSHOT_REPLACE="new_snapshot_value"

BUILD_VERSION_SEARCH="old_build_version"
BUILD_VERSION_REPLACE="new_build_version"

STREAM_NAME_SEARCH="old_stream_name"
STREAM_NAME_REPLACE="new_stream_name"

WORKSPACE="/path/to/your/workspace"

# Variables for Creating the Properties File
TEMPLATES_DIR="ccd_src/bin/templates"
SOURCE_FILE="mdmce_12.0.12.properties"
TARGET_FILE="mdmce_${BUILD_VERSION_REPLACE}.properties"

# Additional replacements for TARGET_FILE
TARGET_FILE_STREAM_REPLACE="new_stream_name"
TARGET_FILE_BUILD_VERSION_REPLACE="new_build_version"

# Navigate to the workspace directory
cd $WORKSPACE

# 1. Replace SNAPSHOT values in all files, excluding .metadata and .jazz directories
echo "Replacing SNAPSHOT values in all files..."
find . -type f ! -path "./.metadata/*" ! -path "./.jazz/*" -exec sed -i "s/$SNAPSHOT_SEARCH/$SNAPSHOT_REPLACE/g" {} +

# 2. Replace build version in all files except .templates, excluding .metadata and .jazz directories
echo "Replacing build version in all files except .templates files..."
find . -type f ! -name "*.templates" ! -path "./.metadata/*" ! -path "./.jazz/*" -exec sed -i "s/$BUILD_VERSION_SEARCH/$BUILD_VERSION_REPLACE/g" {} +

# 3. Replace stream name in all files except .templates, excluding .metadata and .jazz directories
echo "Replacing stream name in all files except .templates files..."
find . -type f ! -name "*.templates" ! -path "./.metadata/*" ! -path "./.jazz/*" -exec sed -i "s/$STREAM_NAME_SEARCH/$STREAM_NAME_REPLACE/g" {} +

# Optional: Output the list of modified files
echo "Modified files containing new snapshot value:"
find . -type f -exec grep -l "$SNAPSHOT_REPLACE" {} +

echo "Modified files containing new build version:"
find . -type f ! -name "*.templates" -exec grep -l "$BUILD_VERSION_REPLACE" {} +

echo "Modified files containing new stream name:"
find . -type f ! -name "*.templates" -exec grep -l "$STREAM_NAME_REPLACE" {} +

# Navigate to the templates directory to create the properties file
cd $TEMPLATES_DIR

# Check if the source file exists
if [ -f "$SOURCE_FILE" ]; then
    # Copy the source file to create the new properties file
    cp "$SOURCE_FILE" "$TARGET_FILE"
    echo "Created $TARGET_FILE as a copy of $SOURCE_FILE"
    
    # Perform additional replacements in the TARGET_FILE
    echo "Replacing RTC_stream with $TARGET_FILE_STREAM_REPLACE in $TARGET_FILE..."
    sed -i "s/RTC_stream/$TARGET_FILE_STREAM_REPLACE/g" "$TARGET_FILE"
    
    echo "Replacing 12.0.12 with $TARGET_FILE_BUILD_VERSION_REPLACE in $TARGET_FILE..."
    sed -i "s/12.0.12/$TARGET_FILE_BUILD_VERSION_REPLACE/g" "$TARGET_FILE"
    
    echo "Updated $TARGET_FILE with new stream name and build version."
else
    echo "Source file $SOURCE_FILE does not exist. Cannot create $TARGET_FILE."
fi
