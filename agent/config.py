"""Configuration for the `ConversableAgent` instances"""

import os
from typing import Annotated, Callable

from autogen import ConversableAgent as __CA
from autogen import config_list_from_json as __clj
from autogen import register_function as __rf
from autogen import filter_config as __fc
from pydantic import BaseModel, Field


def get_agents(
    validator_list: str,
    current_term_id: str,
    aggregate_fn: Callable[[str, str], str],
) -> tuple[__CA, __CA]:
    """Return a tuple of pre-configured `user_proxy` and `aggregator` agents"""

    conf_list = [
        {k: os.path.expandvars(v) for k, v in m.items()}
        for m in __clj("config_list.json", "agent/")
    ]
    aggregator_conf = {
        "config_list": conf_list,
        "temperature": 0,
        "timeout": 500,
    }

    with open("agent/system_msg.txt", "r") as file:
        aggregator_msg = file.read()

    user_proxy = __CA(
        name="User",
        llm_config=None,
        is_termination_msg=lambda msg: "TERMINATE"
        in (msg.get("content") or "").strip(),
        human_input_mode="NEVER",
        default_auto_reply="CONTINUE",
    )

    aggregator = __CA(
        "aggregator",
        system_message=aggregator_msg.format(
            schemas=validator_list, current_term_id=current_term_id
        ),
        max_consecutive_auto_reply=5,
        llm_config=aggregator_conf,
        default_auto_reply="Oops, it seems like I ran into an error, please make sure to ask a specific question.",
    )

    class AggregatorInput(BaseModel):
        collection_name: Annotated[
            str, Field(description="The name of the collection to aggregate")
        ]
        pipeline: Annotated[
            str,
            Field(
                description="The pipeline to apply, must be a valid MongoDB JSON list representing a pipeline"
            ),
        ]

    def aggregate(
        input: Annotated[AggregatorInput, "Input to the aggregation pipeline"]
    ) -> str:
        """
        Run a MongoDB aggregation pipeline given a pipeline and a collection name.

        :param collection_name: the name of the collection to aggregate
        :param pipeline: the pipeline to apply, must be a valid MongoDB JSON document

        :return: a list of documents that match the pipeline
        """
        return aggregate_fn(input.collection_name, input.pipeline)

    __rf(
        aggregate,
        caller=aggregator,
        executor=user_proxy,
        name="aggregate",
        description="Aggregation function to run a MongoDB aggregation pipeline on a collection",
    )

    return user_proxy, aggregator
