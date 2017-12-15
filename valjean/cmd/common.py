'''Common utilities for :program:`valjean` commands.'''


class Action:

    def register(self, parser):
        '''Register options for this command in the parser.'''
        raise NotImplementedError('Action must be subclassed.')

    def process(self, args, config):
        '''Process the arguments to this command.'''
        raise NotImplementedError('Action must be subclassed.')


class TaskFactory:

    def __init__(self, config_prefix, task_cls):
        self.config_prefix = config_prefix
        self.task_cls = task_cls

    def make_task(self, config, name):
        return self.task_cls.from_config(name=name, config=config)

    def make_tasks(self, config, targets=None):
        return [self.make_task(config, name)
                for _, name in self._config_sections(config, targets)]

    def _config_sections(self, config, targets=None):
        '''Extract configuration sections for this command.

        This generator queries the configuration for relevant sectionsi, where
        "relevant" means that the section name starts with the `config_prefix`
        string used at construction. If the `targets` parameter is `None`, all
        relevant configuration sections will be yielded; otherwise, only those
        matching target will.

        :param Config config: The configuration object.
        :param targets: A collection of targets, or `None` for all of them.
        :type targets: collection or None
        :returns: An iterable over `(section_name, target_name)` pairs.
        '''
        if targets:
            yield from (
                x for target in targets
                for x in config.sections_by_prefix(self.config_prefix, target)
            )
        else:
            yield from config.sections_by_prefix(self.config_prefix)
