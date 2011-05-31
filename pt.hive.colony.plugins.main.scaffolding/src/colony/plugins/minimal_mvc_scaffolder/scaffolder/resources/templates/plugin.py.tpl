import colony.base.plugin_system
import colony.base.decorators

class ${out value=scaffold_attributes.class_name /}Plugin(colony.base.plugin_system.Plugin):
    id = "${out value=scaffold_attributes.plugin_id /}"
    name = "${out value=scaffold_attributes.short_name /} Plugin"
    short_name = "${out value=scaffold_attributes.short_name /}"
    version = "${out value=scaffold_attributes.plugin_version /}"
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "web.mvc_service"
    ]
    dependencies = [
        colony.base.plugin_system.PluginDependency("pt.hive.colony.plugins.web.mvc.utils", "${out value=scaffold_attributes.plugin_version /}")
    ]
    main_modules = [
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_controllers",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_entity_models",
        "${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system"
    ]

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system
        self.${out value=scaffold_attributes.variable_name /} = ${out value=scaffold_attributes.backend_namespace /}.${out value=scaffold_attributes.variable_name /}_system.${out value=scaffold_attributes.class_name /}(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.${out value=scaffold_attributes.variable_name /}.load_components()

    @colony.base.decorators.inject_dependencies("${out value=scaffold_attributes.plugin_id /}", "${out value=scaffold_attributes.plugin_version /}")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def get_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_patterns()

    def get_communication_patterns(self):
        return ()

    def get_resource_patterns(self):
        return self.${out value=scaffold_attributes.variable_name /}.get_resource_patterns()

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin
