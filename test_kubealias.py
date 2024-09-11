import unittest
import kubealias

class TestKubealias(unittest.TestCase):

    pairs = {
        'gepo': 'kubectl get pods',
        'gepoanwa': 'kubectl get pods --all-namespaces --watch',

    }

    def test_upper(self):
        for k, v in self.pairs.items():
            self.assertEqual(kubealias.create_command(['does not matter',k]), v)

if __name__ == '__main__':
    unittest.main()