import os
import sys
import unittest


# Ensure the project root is on sys.path so ``main`` can be imported when tests
# are run from different working directories.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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
        """When no alias is given, the help message should be returned."""
        result = main.create_command(["prog"])
        self.assertIn("Usage:", result)

    def test_unknown_alias_returns_message(self) -> None:
        """An unknown alias should return an informative error message."""
        result = main.create_command(["prog", "gezz"])
        self.assertEqual(
            result,
            "echo \"Alias not found: 'zz'. Call the script without arguments for help.\"",
        )

    def test_ff_alias_builds_fzf_command(self) -> None:
        """The special ``ff`` alias should inject the fzf command snippet."""
        result = main.create_command(["prog", "geffpo"])
        snippet = "$(kubectl get pods | fzftab | awk '{print $1}')"
        self.assertIn(snippet, result)
        self.assertTrue(result.startswith("kubectl get "))
        self.assertTrue(result.endswith(" pods"))


if __name__ == "__main__":
    unittest.main()

