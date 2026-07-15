#!/bin/sh
# Copies the endpoint + model deployment name that 'azd up' just provisioned
# into the lab's Python/.env, so the task scripts can read them.
#
# azd runs this automatically after provisioning (see azure.yaml). It sets the
# bicep outputs as environment variables, which we read here.

set -e

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
env_path="$script_dir/../Python/.env"
example_path="$script_dir/../Python/.env.example"

# Start from the existing .env, or the example if there isn't one yet.
if [ ! -f "$env_path" ]; then
    if [ -f "$example_path" ]; then cp "$example_path" "$env_path"; else : > "$env_path"; fi
fi

set_env_value() {
    key="$1"
    value="$2"
    [ -z "$value" ] && return 0
    if grep -qE "^[[:space:]]*$key[[:space:]]*=" "$env_path"; then
        # Replace the existing line.
        tmp="${env_path}.tmp"
        sed "s|^[[:space:]]*$key[[:space:]]*=.*|$key=$value|" "$env_path" > "$tmp"
        mv "$tmp" "$env_path"
    else
        printf '%s=%s\n' "$key" "$value" >> "$env_path"
    fi
}

set_env_value "PROJECT_ENDPOINT" "$PROJECT_ENDPOINT"
set_env_value "MODEL_DEPLOYMENT_NAME" "$MODEL_DEPLOYMENT_NAME"

echo "Updated $env_path with your provisioned PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME."
echo "Task 3 also needs a grounded agent: run 'python setup/bootstrap_agent.py' to create it."
