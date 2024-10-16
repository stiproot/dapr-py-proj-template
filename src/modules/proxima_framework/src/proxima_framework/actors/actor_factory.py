from typing import Optional, Awaitable, T
from dapr.actor import ActorProxy, ActorId
from .proc_actor_interface import ProcActorInterface
from .proc_actor import ProcActor


def create_proxy(actor_type: str, actor_id: str, actor_interface: T) -> "ActorProxy":
    proxy = ActorProxy.create(
        actor_type=actor_type,
        actor_id=ActorId(actor_id),
        actor_interface=actor_interface,
    )
    return proxy


def create_proc_proxy(actor_id: str) -> ProcActor:
    return create_proxy(ProcActor.__name__, actor_id, ProcActorInterface)
