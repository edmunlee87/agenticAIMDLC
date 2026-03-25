"""Platform core services package.

Exports all base service, controller, bridge, runtime component, and widget
base classes for use by SDK implementations.

Import order for consumers:
    from platform_core.services import BaseService, BaseStorageService, BaseRegistryService
    from platform_core.services import BaseReviewComponent, BaseSparkService
    from platform_core.services import BaseController, BaseBridge
    from platform_core.services import BaseRuntimeComponent, BaseWidgetComponent
"""

from .base_bridge import BaseBridge
from .base_controller import BaseController
from .base_runtime_component import BaseRuntimeComponent
from .base_service import (
    BaseRegistryService,
    BaseReviewComponent,
    BaseService,
    BaseSparkService,
    BaseStorageService,
)
from .base_widget_component import BaseWidgetComponent

__all__ = [
    "BaseService",
    "BaseStorageService",
    "BaseRegistryService",
    "BaseReviewComponent",
    "BaseSparkService",
    "BaseController",
    "BaseBridge",
    "BaseRuntimeComponent",
    "BaseWidgetComponent",
]
