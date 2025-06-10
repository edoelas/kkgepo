import os
import sys
import unittest


# Ensure the project root is on sys.path so ``main`` can be imported when tests
# are run from different working directories.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Ensure tests use the repository's aliases file
os.environ["KKGEPO_ALIASES"] = os.path.join(ROOT_DIR, "aliases.yaml")

import main


class TestKubealias(unittest.TestCase):
    """Unit tests for the :func:`main.create_command` function."""

    basic_pairs = {
        "gepo": "kubectl get pods",
        "gepoanwa": "kubectl get pods --all-namespaces --watch",
        # fetching resources
        "gest": "kubectl get statefulset",
        "gesl": "kubectl get --show-labels",
        "gepoow": "kubectl get pods -o=wide",
        "gestan": "kubectl get statefulset --all-namespaces",
        # describe
        "deno": "kubectl describe nodes",
        "decr": "kubectl describe clusterrole",
        # apply with flags
        "afseoy": "kubectl apply --recursive -f secret -o=yaml",
    }

    def test_basic_aliases(self) -> None:
        """Ensure simple aliases map to the expected kubectl command."""
        for alias, expected in self.basic_pairs.items():
            with self.subTest(alias=alias):
                self.assertEqual(
                    main.create_command(["prog", alias]),
                    expected,
                )

    def test_help_shown_when_no_alias_provided(self) -> None:
        """When no alias is given, the help message should be printed."""
        from io import StringIO
        import contextlib

        out = StringIO()
        with contextlib.redirect_stdout(out):
            result = main.create_command(["prog"])
        self.assertIsNone(result)
        self.assertIn("Usage:", out.getvalue())

    def test_unknown_alias_returns_message(self) -> None:
        """An unknown alias should print an informative error message."""
        from io import StringIO
        import contextlib

        out = StringIO()
        with contextlib.redirect_stdout(out):
            result = main.create_command(["prog", "gezz"])
        self.assertIsNone(result)
        self.assertIn("Alias not found", out.getvalue())

    def test_ff_alias_builds_fzf_command(self) -> None:
        """The special ``ff`` alias should inject the fzf command snippet."""
        result = main.create_command(["prog", "geffpo"])
        snippet = (
            "$(kubectl get pods | fzf --height=13 --border --reverse --pointer '>' "
            "--header-lines=1 --color 'header:reverse' | awk '{print $1}')"
        )
        self.assertIn(snippet, result)
        self.assertTrue(result.startswith("kubectl get "))
        self.assertTrue(result.endswith(" pods"))

    def test_aliases_loaded_from_env_variable(self) -> None:
        """Module should load aliases from the path specified in ``KKGEPO_ALIASES``."""
        import importlib
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            tmp.write("commands:\n  xx: foo\n")
            temp_path = tmp.name

        try:
            os.environ["KKGEPO_ALIASES"] = temp_path
            importlib.reload(main)
            self.assertEqual(main.create_command(["prog", "xx"]), "kubectl foo")
        finally:
            os.environ["KKGEPO_ALIASES"] = os.path.join(ROOT_DIR, "aliases.yaml")
            importlib.reload(main)
            Path(temp_path).unlink()

    def test_error_when_env_var_missing(self) -> None:
        """Reloading the module without ``KKGEPO_ALIASES`` prints an error."""
        import importlib
        from io import StringIO
        import contextlib

        os.environ.pop("KKGEPO_ALIASES", None)
        stderr = StringIO()
        with contextlib.redirect_stderr(stderr):
            importlib.reload(main)
        self.assertIn("KKGEPO_ALIASES", stderr.getvalue())
        os.environ["KKGEPO_ALIASES"] = os.path.join(ROOT_DIR, "aliases.yaml")
        importlib.reload(main)

    def test_main_executes_command(self) -> None:
        """``main.main`` should execute the generated command by default."""
        from unittest import mock

        with mock.patch("subprocess.run") as run_mock:
            main.main(["prog", "gepo"])
            run_mock.assert_called_once_with("kubectl get pods", shell=True, check=False)

    def test_main_print_flag(self) -> None:
        """When ``--print`` is provided the command is printed only."""
        from io import StringIO
        from unittest import mock
        out = StringIO()
        with mock.patch("subprocess.run") as run_mock, mock.patch("sys.stdout", out):
            main.main(["prog", "--print", "gepo"])
            run_mock.assert_not_called()
        self.assertEqual(out.getvalue().strip(), "kubectl get pods")


if __name__ == "__main__":
    unittest.main()

