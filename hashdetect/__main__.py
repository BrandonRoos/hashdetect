"""Entry point for hashdetect. No longer need to type CLI, use `python -m hashdetect` to run the CLI."""
from hashdetect.cli import main
raise SystemExit(main())

# python - m hashdetect runs the package directly. Python looks for __main__.py inside a package and runs it when you -m the package itself. Same pattern as Java's META-INF/MANIFEST.MF Main-Class declaration, but lighter weight.
