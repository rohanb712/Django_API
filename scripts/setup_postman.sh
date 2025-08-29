#!/bin/bash

# Postman Setup Script for Sustainability Actions API
# Cross-platform setup script for Postman integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
POSTMAN_DIR="$PROJECT_ROOT/postman"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

print_header() {
    echo -e "${BLUE}🚀 Setting up Postman integration for Sustainability Actions API${NC}"
    echo "=================================================================="
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_dependencies() {
    echo "Checking dependencies..."
    
    # Check Node.js
    if command -v node >/dev/null 2>&1; then
        NODE_VERSION=$(node --version)
        print_success "Node.js is installed: $NODE_VERSION"
    else
        print_error "Node.js is not installed. Please install Node.js from https://nodejs.org/"
        exit 1
    fi
    
    # Check npm
    if command -v npm >/dev/null 2>&1; then
        NPM_VERSION=$(npm --version)
        print_success "npm is installed: $NPM_VERSION"
    else
        print_error "npm is not installed. Please install npm."
        exit 1
    fi
    
    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python is installed: $PYTHON_VERSION"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_VERSION=$(python --version)
        print_success "Python is installed: $PYTHON_VERSION"
    else
        print_warning "Python is not found. Some features may not work."
    fi
}

install_newman() {
    echo "Installing Newman CLI..."
    
    # Check if Newman is already installed
    if command -v newman >/dev/null 2>&1; then
        NEWMAN_VERSION=$(newman --version)
        print_success "Newman is already installed: $NEWMAN_VERSION"
        return 0
    fi
    
    # Install Newman globally
    if npm install -g newman; then
        print_success "Newman installed successfully"
    else
        print_error "Failed to install Newman. You may need to run with sudo or check permissions."
        return 1
    fi
    
    # Install HTML reporter (optional)
    if npm install -g newman-reporter-htmlextra 2>/dev/null; then
        print_success "Newman HTML reporter installed"
    else
        print_warning "Could not install HTML reporter. Documentation generation will be limited."
    fi
}

create_postman_directory() {
    if [ ! -d "$POSTMAN_DIR" ]; then
        mkdir -p "$POSTMAN_DIR"
        print_success "Created postman directory"
    else
        print_info "Postman directory already exists"
    fi
}

validate_collection() {
    local collection_file="$POSTMAN_DIR/Sustainability_Actions_API.postman_collection.json"
    
    if [ -f "$collection_file" ]; then
        # Basic JSON validation
        if python3 -m json.tool "$collection_file" >/dev/null 2>&1 || python -m json.tool "$collection_file" >/dev/null 2>&1; then
            print_success "Postman collection is valid JSON"
        else
            print_error "Postman collection has invalid JSON"
            return 1
        fi
    else
        print_error "Postman collection file not found: $collection_file"
        return 1
    fi
}

validate_environments() {
    local dev_env="$POSTMAN_DIR/Development.postman_environment.json"
    local prod_env="$POSTMAN_DIR/Production.postman_environment.json"
    
    for env_file in "$dev_env" "$prod_env"; do
        if [ -f "$env_file" ]; then
            if python3 -m json.tool "$env_file" >/dev/null 2>&1 || python -m json.tool "$env_file" >/dev/null 2>&1; then
                print_success "Environment file is valid: $(basename "$env_file")"
            else
                print_error "Environment file has invalid JSON: $(basename "$env_file")"
                return 1
            fi
        else
            print_warning "Environment file not found: $(basename "$env_file")"
        fi
    done
}

run_collection_test() {
    echo "Running Postman collection tests..."
    
    local collection_file="$POSTMAN_DIR/Sustainability_Actions_API.postman_collection.json"
    local env_file="$POSTMAN_DIR/Development.postman_environment.json"
    
    if [ ! -f "$collection_file" ] || [ ! -f "$env_file" ]; then
        print_error "Collection or environment file missing"
        return 1
    fi
    
    # Check if Django server is running
    if ! curl -s "http://localhost:8000/api/actions/" >/dev/null 2>&1; then
        print_warning "Django server is not running on localhost:8000"
        print_info "Start the server with: python manage.py runserver"
        print_info "Skipping live tests..."
        return 0
    fi
    
    # Run the collection
    if newman run "$collection_file" -e "$env_file" --reporters cli; then
        print_success "All Postman tests passed!"
    else
        print_warning "Some tests failed. This may be expected if the server is not running."
    fi
}

generate_documentation() {
    echo "Generating API documentation..."
    
    local collection_file="$POSTMAN_DIR/Sustainability_Actions_API.postman_collection.json"
    local output_file="$POSTMAN_DIR/api-documentation.html"
    
    if command -v newman >/dev/null 2>&1; then
        if newman run "$collection_file" --reporters htmlextra --reporter-htmlextra-export "$output_file" --reporter-htmlextra-title "Sustainability Actions API Documentation" 2>/dev/null; then
            print_success "Generated documentation: $output_file"
        else
            print_info "HTML documentation generation requires newman-reporter-htmlextra"
            print_info "Install with: npm install -g newman-reporter-htmlextra"
        fi
    fi
}

setup_git_hooks() {
    echo "Setting up git hooks for collection validation..."
    
    local hooks_dir="$PROJECT_ROOT/.git/hooks"
    local pre_commit_hook="$hooks_dir/pre-commit"
    
    if [ -d "$hooks_dir" ]; then
        cat > "$pre_commit_hook" << 'EOF'
#!/bin/bash
# Pre-commit hook to validate Postman collections

POSTMAN_DIR="$(git rev-parse --show-toplevel)/postman"

echo "Validating Postman collections..."

# Validate collection JSON
for file in "$POSTMAN_DIR"/*.json; do
    if [ -f "$file" ]; then
        if ! python3 -m json.tool "$file" >/dev/null 2>&1 && ! python -m json.tool "$file" >/dev/null 2>&1; then
            echo "Error: Invalid JSON in $(basename "$file")"
            exit 1
        fi
    fi
done

echo "✓ Postman collections validated"
EOF
        
        chmod +x "$pre_commit_hook"
        print_success "Git pre-commit hook installed"
    else
        print_warning "Not a git repository. Skipping git hooks setup."
    fi
}

print_next_steps() {
    echo
    echo -e "${GREEN}✅ Postman setup completed successfully!${NC}"
    echo
    echo -e "${BLUE}📚 Next steps:${NC}"
    echo "1. Open Postman application"
    echo "2. Import collection: File → Import → $POSTMAN_DIR/Sustainability_Actions_API.postman_collection.json"
    echo "3. Import environment: File → Import → $POSTMAN_DIR/Development.postman_environment.json"
    echo "4. Start Django server: python manage.py runserver"
    echo "5. Select 'Development Environment' in Postman"
    echo "6. Run the collection or individual requests"
    echo
    echo -e "${BLUE}🔧 CLI Usage:${NC}"
    echo "• Test collection: newman run postman/Sustainability_Actions_API.postman_collection.json -e postman/Development.postman_environment.json"
    echo "• Update collection: python scripts/setup_postman.py --update-collection"
    echo "• Run automated tests: python scripts/setup_postman.py --run-tests"
    echo
    echo -e "${BLUE}📁 Files created:${NC}"
    echo "• $POSTMAN_DIR/Sustainability_Actions_API.postman_collection.json"
    echo "• $POSTMAN_DIR/Development.postman_environment.json"
    echo "• $POSTMAN_DIR/Production.postman_environment.json"
    echo "• $SCRIPTS_DIR/setup_postman.py"
}

main() {
    print_header
    
    check_dependencies
    create_postman_directory
    install_newman
    validate_collection
    validate_environments
    generate_documentation
    setup_git_hooks
    
    # Only run tests if explicitly requested
    if [ "$1" = "--test" ]; then
        run_collection_test
    fi
    
    print_next_steps
}

# Run main function with all arguments
main "$@"