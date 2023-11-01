from typing import Any
from typing import Dict
from typing import Optional

import requests
from loguru import logger

from app.connectors.utils import get_connector_info_from_db


def verify_shuffle_credentials(attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifies the connection to Shuffle service.

    Returns:
        dict: A dictionary containing 'connectionSuccessful' status and 'authToken' if the connection is successful.
    """
    logger.info(
        f"Verifying the Shuffle connection to {attributes['connector_url']}",
    )
    try:
        headers = {
            "Authorization": f"Bearer {attributes['connector_api_key']}",
        }
        shuffle_apps = requests.get(
            f"{attributes['connector_url']}/api/v1/apps/authentication",
            headers=headers,
            verify=False,
        )
        if shuffle_apps.status_code == 200:
            logger.info(
                f"Connection to {attributes['connector_url']} successful",
            )
            return {"connectionSuccessful": True, "message": "Shuffle connection successful"}
        else:
            logger.error(
                f"Connection to {attributes['connector_url']} failed with error: {shuffle_apps.text}",
            )
            return {
                "connectionSuccessful": False,
                "message": f"Connection to {attributes['connector_url']} failed with error: {shuffle_apps.text}",
            }
    except Exception as e:
        logger.error(
            f"Connection to {attributes['connector_url']} failed with error: {e}",
        )
        return {"connectionSuccessful": False, "message": f"Connection to {attributes['connector_url']} failed with error: {e}"}


def verify_shuffle_connection(connector_name: str) -> str:
    """
    Returns if connection to Shuffle service is successful.
    """
    logger.info("Getting Shuffle authentication token")
    attributes = get_connector_info_from_db(connector_name)
    if attributes is None:
        logger.error("No Shuffle connector found in the database")
        return None
    return verify_shuffle_credentials(attributes)


def send_get_request(endpoint: str, params: Optional[Dict[str, Any]] = None, connector_name: str = "Shuffle") -> Dict[str, Any]:
    """
    Sends a GET request to the Shuffle service.

    Args:
        endpoint (str): The endpoint to send the GET request to.
        params (Optional[Dict[str, Any]], optional): The parameters to send with the GET request. Defaults to None.
        connector_name (str, optional): The name of the connector to use. Defaults to "Shuffle".

    Returns:
        Dict[str, Any]: The response from the GET request.
    """
    logger.info(f"Sending GET request to {endpoint}")
    attributes = get_connector_info_from_db(connector_name)
    if attributes is None:
        logger.error("No Graylog connector found in the database")
        return None
    try:
        HEADERS = {
            "Authorization": f"Bearer {attributes['connector_api_key']}",
        }
        response = requests.get(
            f"{attributes['connector_url']}{endpoint}",
            headers=HEADERS,
            params=params,
            verify=False,
        )
        return {"data": response.json(), "success": True, "message": "Successfully retrieved data"}
    except Exception as e:
        logger.error(f"Failed to send GET request to {endpoint} with error: {e}")
        return {"success": False, "message": f"Failed to send GET request to {endpoint} with error: {e}"}


def send_post_request(endpoint: str, data: Dict[str, Any] = None, connector_name: str = "Graylog") -> Dict[str, Any]:
    """
    Sends a POST request to the Graylog service.

    Args:
        endpoint (str): The endpoint to send the POST request to.
        data (Dict[str, Any]): The data to send with the POST request.
        connector_name (str, optional): The name of the connector to use. Defaults to "Graylog".

    Returns:
        Dict[str, Any]: The response from the POST request.
    """
    logger.info(f"Sending POST request to {endpoint}")
    attributes = get_connector_info_from_db(connector_name)
    if attributes is None:
        logger.error("No Graylog connector found in the database")
        return {"success": False, "message": "No Graylog connector found in the database"}

    try:
        HEADERS = {
            "Authorization": f"Bearer {attributes['connector_api_key']}",
        }
        response = requests.post(
            f"{attributes['connector_url']}{endpoint}",
            headers=HEADERS,
            auth=(
                attributes["connector_username"],
                attributes["connector_password"],
            ),
            json=data,
            verify=False,
        )

        if response.status_code == 204:
            return {"data": None, "success": True, "message": "Successfully completed request with no content"}
        else:
            return {
                "data": response.json(),
                "success": False if response.status_code >= 400 else True,
                "message": "Successfully retrieved data" if response.status_code < 400 else "Failed to retrieve data",
            }
    except Exception as e:
        logger.debug(f"Response: {response}")
        logger.error(f"Failed to send POST request to {endpoint} with error: {e}")
        return {"success": False, "message": f"Failed to send POST request to {endpoint} with error: {e}"}


def send_delete_request(endpoint: str, params: Optional[Dict[str, Any]] = None, connector_name: str = "Graylog") -> Dict[str, Any]:
    """
    Sends a DELETE request to the Graylog service.

    Args:
        endpoint (str): The endpoint to send the DELETE request to.
        params (Optional[Dict[str, Any]], optional): The parameters to send with the DELETE request. Defaults to None.
        connector_name (str, optional): The name of the connector to use. Defaults to "Graylog".

    Returns:
        Dict[str, Any]: The response from the DELETE request.
    """
    logger.info(f"Sending DELETE request to {endpoint}")
    attributes = get_connector_info_from_db(connector_name)
    if attributes is None:
        logger.error("No Graylog connector found in the database")
        return None
    try:
        HEADERS = {
            "Authorization": f"Bearer {attributes['connector_api_key']}",
        }
        response = requests.delete(
            f"{attributes['connector_url']}{endpoint}",
            headers=HEADERS,
            auth=(
                attributes["connector_username"],
                attributes["connector_password"],
            ),
            params=params,
            verify=False,
        )
        return {"data": response.json(), "success": True, "message": "Successfully retrieved data"}
    except Exception as e:
        logger.error(f"Failed to send DELETE request to {endpoint} with error: {e}")
        return {"success": False, "message": f"Failed to send DELETE request to {endpoint} with error: {e}"}


def send_put_request(endpoint: str, data: Optional[Dict[str, Any]] = None, connector_name: str = "Graylog") -> Dict[str, Any]:
    """
    Sends a PUT request to the Graylog service.

    Args:
        endpoint (str): The endpoint to send the PUT request to.
        data (Optional[Dict[str, Any]]): The data to send with the PUT request.
        connector_name (str, optional): The name of the connector to use. Defaults to "Graylog".

    Returns:
        Dict[str, Any]: The response from the PUT request.
    """
    logger.info(f"Sending PUT request to {endpoint}")
    attributes = get_connector_info_from_db(connector_name)
    if attributes is None:
        logger.error("No Graylog connector found in the database")
        return None
    try:
        HEADERS = {
            "Authorization": f"Bearer {attributes['connector_api_key']}",
        }
        response = requests.put(
            f"{attributes['connector_url']}{endpoint}",
            headers=HEADERS,
            auth=(
                attributes["connector_username"],
                attributes["connector_password"],
            ),
            json=data,
            verify=False,
        )
        return {"data": response.json(), "success": True, "message": "Successfully retrieved data"}
    except Exception as e:
        logger.error(f"Failed to send PUT request to {endpoint} with error: {e}")
        return {"success": False, "message": f"Failed to send PUT request to {endpoint} with error: {e}"}