#!/bin/bash

# 配置
GITLAB_URL="http://220.185.136.6:9001"
ACCESS_TOKEN=""
SOURCE_BRANCH="dev"
TARGET_BRANCH="main"
TAG_PREFIX="release-1.0.0"
TAG_MESSAGE="New release"

# 使用 GitLab API 获取所有项目的列表
echo "Fetching projects from GitLab..."
response=$(curl --silent --header "Private-Token: $ACCESS_TOKEN" "$GITLAB_URL/api/v4/projects?simple=true&per_page=100")

# 检查未过滤的项目列表
echo "Unfiltered projects:"
echo "$response" | jq -r '.[] | .name_with_namespace'

# 过滤项目列表
echo "Filtered projects:"
projects=$(echo "$response" | jq -r '.[] | .path_with_namespace')
echo "$projects"

# 遍历所有项目
echo "Found projects:"
echo "$projects"
for project in $projects; do
    echo "====================================="
    echo "Processing project: $project"
    
    repo_name=$(basename "$project")
    if [ ! -d "$repo_name" ]; then
        # 如果项目目录不存在，则克隆项目
        echo "Cloning project: $project"
        git clone "$GITLAB_URL/$project.git" || { echo "Failed to clone $project"; continue; }
    fi
    
    cd "$repo_name" || continue

    # 尝试最多三次的简单重试机制
    retry_count=0
    max_retries=3
    until [ "$retry_count" -ge "$max_retries" ]
    do
        git checkout $SOURCE_BRANCH && git pull origin $SOURCE_BRANCH && break
        retry_count=$((retry_count+1))
        echo "Retry $retry_count of $max_retries for git pull $SOURCE_BRANCH"
        sleep 2
    done

    git checkout $TARGET_BRANCH && git pull origin $TARGET_BRANCH

    # 合并 develop 到 main
    if ! git merge $SOURCE_BRANCH --no-ff -m "Merging changes from $SOURCE_BRANCH to $TARGET_BRANCH"; then
        echo "Merge failed for project: $project"
        cd ..
        rm -rf "$repo_name"
        continue
    fi

    echo "Merge successful"
    TAG_NAME="${TAG_PREFIX}"
    git tag -a "$TAG_NAME" -m "$TAG_MESSAGE"
    
    # 推送更改和新标签到远程仓库，带简单重试机制
    retry_count=0
    until [ "$retry_count" -ge "$max_retries" ]
    do
        git push origin $TARGET_BRANCH && git push origin "$TAG_NAME" && break
        retry_count=$((retry_count+1))
        echo "Retry $retry_count of $max_retries for git push"
        sleep 2
    done

    # 退出项目目录
    cd ..

    # 根据需要可以删除本地仓库副本
    #rm -rf "$repo_name"

    echo "====================================="
done
