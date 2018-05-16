from __future__ import print_function, unicode_literals, with_statement, division

from django.core.management.base import BaseCommand

from simple_scaffold.scaffold import Scaffold


class Command(BaseCommand):
    # option_list = BaseCommand.option_list + (
        # make_option('--model', default=None, dest='model',
                    # help="""model name - only one model name per run is allowed. \n
            # It requires additional fields parameters:

            # char - CharField \t\t\t\t
            # text - TextField \t\t\t\t
            # int - IntegerFIeld \t\t\t\t
            # decimal -DecimalField \t\t\t\t
            # datetime - DateTimeField \t\t\t\t
            # foreign - ForeignKey \t\t\t\t

            # Example usages: \t\t\t\t

                # --model forum char:title  text:body int:posts datetime:create_date \t\t
                # --model blog foreign:blog:Blog, foreign:post:Post, foreign:added_by:User \t\t
                # --model finance decimal:total_cost:10:2

            # """),
    # )

    def add_arguments(self, parser):
        parser.add_argument('app', help='hellow')
        parser.add_argument(
            '-M',
            '--model',
            dest='model',
            nargs='+',
            help="""model name - only one model name per run is allowed. \n
            It requires additional fields parameters:

            char - CharField \t\t\t\t
            text - TextField \t\t\t\t
            int - IntegerFIeld \t\t\t\t
            decimal -DecimalField \t\t\t\t
            datetime - DateTimeField \t\t\t\t
            foreign - ForeignKey \t\t\t\t

            Example usages: \t\t\t\t

                --model forum char:title  text:body int:posts datetime:create_date \t\t
                --model blog foreign:blog:Blog, foreign:post:Post, foreign:added_by:User \t\t
                --model finance decimal:total_cost:10:2

            """
        )

    def handle(self, *args, **options):
        # if len(args) == 0:
            # print("You must provide app name. For example:\n\npython manage.py scallfold my_app\n")
            # return
        # scaffold = Scaffold(args[0], options['model'], args)
        # scaffold.run()
        if options['model']:
            scaffold = Scaffold(options['app'], options['model'][0], options['model'][1:])
            scaffold.run()

    def get_version(self):
        return 'django-common version: {0}'.format(0.1)
