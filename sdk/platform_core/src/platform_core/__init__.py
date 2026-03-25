"""
platform_core
=============
Runtime resolver, controllers, bridges, base service classes, and utilities
for the MDLC framework.

Import hierarchy (no circular deps):
  platform_contracts <- platform_core.utils
  platform_contracts <- platform_core.schemas
  platform_core.schemas <- platform_core.services.base
  platform_core.schemas <- platform_core.controllers.base
  platform_core.schemas <- platform_core.bridges.base
  platform_core.runtime.config_models <- platform_core.runtime.config_loader
  platform_core.runtime.config_models <- platform_core.runtime.stage_config_resolver
"""
