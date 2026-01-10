$paths = @(
    # Dossiers
    "src",
    "src\models",
    "src\repositories",
    "src\services",
    "src\routes",
    "src\conf",
    "src\utils",
    "tests",
    # Fichiers
    ".env",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "src\__init__.py",
    "src\models\__init__.py",
    "src\repositories\__init__.py",
    "src\services\__init__.py",
    "src\routes\__init__.py",
    "src\conf\__init__.py",
    "src\utils\__init__.py",
    "src\main.py",
    "tests\conftest.py",
    "tests\test_health.py"
)

foreach ($path in $paths) {
    $dir = Split-Path $path
    if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Force -Path $path | Out-Null
    }
}