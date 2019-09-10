#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


class Des:
    def __init__(self):
        self.laravel = "laravel"
        self.vue = "vue"
        self.composer = "composer"
        self.file = os.path.realpath(__file__)

    def checkParams(self):
        return len(sys.argv) <= 1

    def main(self):
        if self.checkParams():
            print("Argumentos no validos o faltantes.")
            sys.exit(1)

        if (
            sys.argv[1] != self.laravel
            and sys.argv[1] != self.vue
            and len(sys.argv) == 2
        ):
            self.scaffold(self.laravel)
            self.scaffold(self.vue)
            return True

        if len(sys.argv) >= 3:
            for i in range(1, len(sys.argv), 2):
                self.scaffold(sys.argv[i], i)

    def scaffold(self, argument, num_arg=None):
        print(argument)
        return getattr(self, "make_" + str(argument))(num_arg)

    def exec_cmd(self, command):
        result = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = result.communicate()

        if result is not None:
            print(
                "El comando {} no existe o fue mal ejecutado.".format(command)
            )
            sys.exit(1)

        return True

    def make_laravel(self, num_arg=None):
        if num_arg is None:
            num_arg = 1

        self.exec_cmd(
            [self.laravel, "new", "api.{}".format(sys.argv[num_arg])]
        )
        os.getcwd(os.getcwd() + "api.{}".format(sys.argv[num_arg]))
        self.exec_cmd(
            [
                self.composer,
                "require",
                "nuwave/lighthouse",
                "mll-lab/laravel-graphql-playground",
            ]
        )
        self.exec_cmd(
            [
                "php",
                "artisan",
                "vendor:publish",
                '--provider="Nuwave\\Lighthouse\\LighthouseServiceProvider"',
            ]
        )
        self.exec_cmd(
            [
                "php",
                "artisan",
                "vendor:publish",
                '--provider="MLL\\GraphQLPlayground\\GraphQLPlaygroundServiceProvider"',
            ]
        )

    def make_vue(self, num_arg=None):
        if num_arg is None:
            num_arg = 1

        self.exec_cmd()


if __name__ == "__main__":
    des = Des()
    des.main()
