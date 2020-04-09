import json
from dynamite_nsm.components.base import exec_strategy
from dynamite_nsm.services.elasticsearch import install, process


def print_message(msg):
    print(msg)


class ElasticsearchInstallStrategy(exec_strategy.BaseExecStrategy):

    def __init__(self, password, heap_size_gigs, install_jdk, stdout, verbose):
        exec_strategy.BaseExecStrategy.__init__(
            self,
            strategy_name="elasticsearch_install",
            strategy_description="Install and secure Elasticsearch.",
            functions=(
                install.install_elasticsearch,
                process.stop,
                print_message,
                print_message
            ),
            arguments=(
                # install.install_elasticsearch
                {
                    "configuration_directory": "/etc/dynamite/elasticsearch/",
                    "install_directory": "/opt/dynamite/elasticsearch/",
                    "log_directory": "/var/log/dynamite/elasticsearch/",
                    "password": str(password),
                    "heap_size_gigs": int(heap_size_gigs),
                    "install_jdk": bool(install_jdk),
                    "create_dynamite_user": True,
                    "stdout": bool(stdout),
                    "verbose": bool(verbose)
                },

                # process.stop
                {
                    "stdout": False
                },

                # print_message
                {
                    "msg": '[+] *** ElasticSearch installed successfully. ***\n'
                },
                # print_message
                {
                    "msg": '[+] Next, Start your cluster: '
                           '\'dynamite start elasticsearch\'.'
                }
            ),
            return_formats=(
                None,
                None,
                None,
                None
            ))


class ElasticsearchUninstallStrategy(exec_strategy.BaseExecStrategy):

    def __init__(self, stdout, prompt_user):
        exec_strategy.BaseExecStrategy.__init__(
            self, strategy_name="elasticsearch_uninstall",
            strategy_description="Uninstall Elasticsearch.",
            functions=(
                install.uninstall_elasticsearch,
                print_message
            ),
            arguments=(
                # install.uninstall_elasticsearch
                {
                    "stdout": bool(stdout),
                    "prompt_user": bool(prompt_user)
                },

                # print_message
                {
                    "msg": '[+] *** ElasticSearch uninstalled successfully. ***\n'
                },
            ),
            return_formats=(
                None,
                None
            )
        )


class ElasticsearchProcessStartStrategy(exec_strategy.BaseExecStrategy):
    def __init__(self, stdout, status):
        exec_strategy.BaseExecStrategy.__init__(
            self, strategy_name="elasticsearch_start",
            strategy_description="Start Elasticsearch process.",
            functions=(
                process.start,
            ),
            arguments=(
                {
                    "stdout": stdout
                }
            ),
            return_formats=(
                None,
            )

        )
        if status:
            self.add_function(
                process.status, {}, return_format="json")


# Test Functions

def run_install_strategy():
    es_elastic_install_strategy = ElasticsearchInstallStrategy(
        password="changeme",
        heap_size_gigs=4,
        install_jdk=False,
        stdout=True,
        verbose=True
    )
    es_elastic_install_strategy.execute_strategy()


def run_uninstall_strategy():
    es_elastic_uninstall_strategy = ElasticsearchUninstallStrategy(
        stdout=True,
        prompt_user=True
    )
    es_elastic_uninstall_strategy.execute_strategy()


def run_process_start_strategy():
    es_elastic_start_strategy = ElasticsearchProcessStartStrategy(
        stdout=True,
        status=True
    )
    es_elastic_start_strategy.execute_strategy()


if __name__ == '__main__':
    run_install_strategy()
    run_process_start_strategy()
    run_uninstall_strategy()
    pass
