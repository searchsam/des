#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


class Des:
    def __init__(self):
        self.holding_names = ["laravel", "vue", "composer"]
        self.file = os.path.realpath(__file__)
        self.dir = os.getcwd()

    def checkParams(self):
        return len(sys.argv) <= 1

    def call(self, argument, num_arg=None):
        return getattr(self, "make_" + str(argument))(num_arg)

    def make_laravel(self, num_arg=None):
        if num_arg is None:
            num_arg = 1

        os.chdir(self.dir)
        print("Laravel")
        self.exec_cmd(
            [self.holding_names[0], "new", "api.{}".format(sys.argv[num_arg])]
        )
        os.chdir(self.dir + "/api.{}".format(sys.argv[num_arg]))
        print("Composer")
        self.exec_cmd(
            [
                self.holding_names[2],
                "require",
                "nuwave/lighthouse",
                "mll-lab/laravel-graphql-playground",
            ]
        )
        print("Lighthouse")
        self.exec_cmd(
            [
                "php",
                "artisan",
                "vendor:publish",
                '--provider="Nuwave\\Lighthouse\\LighthouseServiceProvider"',
            ]
        )
        print("Playground")
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
            num_arg = -1

        os.chdir(self.dir)
        print("Vue")
        os.system(
            "{0} create {1}".format(self.holding_names[1], sys.argv[num_arg])
        )
        os.chdir(self.dir + "/{}".format(sys.argv[num_arg]))
        print("Apollo")
        os.system("{} add apollo".format(self.holding_names[1]))

    def exec_cmd(self, command):
        stdout, stderr = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()

        if stderr is not None:
            print(
                "El comando {} no existe o fue mal ejecutado.".format(
                    command[0]
                )
            )
            sys.exit(1)

        return True

    def scaffold(self):
        if self.checkParams():
            print("Argumentos no validos o faltantes.")
            sys.exit(1)

        if (
            len(sys.argv) == 3
            and sys.argv[2] != self.holding_names[0]
            and sys.argv[2] != self.holding_names[1]
        ):
            self.call(self.holding_names[0])
            self.call(self.holding_names[1])
            return True

        if (
            len(sys.argv) >= 4
            and sys.argv[-1] != self.holding_names[0]
            and sys.argv[-1] != self.holding_names[1]
        ):
            if self.holding_names[0] in sys.argv:
                if (
                    sys.argv[sys.argv.index(self.holding_names[0]) + 1]
                    not in self.holding_names
                ):
                    self.call(
                        self.holding_names[0],
                        sys.argv.index(self.holding_names[0]) + 1,
                    )
                else:
                    self.call(self.holding_names[0])

            if self.holding_names[1] in sys.argv:
                if (
                    sys.argv[sys.argv.index(self.holding_names[1]) + 1]
                    not in self.holding_names
                ):
                    self.call(
                        self.holding_names[1],
                        sys.argv.index(self.holding_names[1]) + 1,
                    )
                else:
                    self.call(self.holding_names[1])

    def docker(self):
        print("Docker")

    def podman(self):
        print("Podman")


if __name__ == "__main__":
    des = Des()

    {"scaffold": des.scaffold, "docker": des.docker, "podman": des.pod}[
        sys.argv[1]
    ]()
