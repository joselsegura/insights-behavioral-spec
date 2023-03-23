Feature: Basic REST API endpoints provided by Insights Results Aggregator


  Background:
    Given REST API service hostname is localhost
      And REST API service port is 8080
      And REST API service prefix is api/v1
      And Insights Results Aggregator service is started in background


  @rest-api @json-check
  Scenario: Check if the main endpoint is reachable (w/o using auth. token)
    Given the system is in default state
     When I access endpoint / using HTTP GET method
     Then The status code of the response is 401
      And The body of the response has the following schema
          """
          {
            "status": {
              "type": "string"
            }
          }
          """
      And The body of the response is the following
          """
          {"status":"Missing auth token"}
          """
     When I terminate Insights Results Aggregator
     Then Insights Results Aggregator process should terminate


  @rest-api @json-check
  Scenario: Check if the main endpoint is reachable (with proper auth. token)
    Given the system is in default state
     When I access endpoint / using HTTP GET method using token for organization 123 account number 456, and user 789
     Then The status code of the response is 200
      And The body of the response has the following schema
          """
          {
            "status": {
              "type": "string"
            }
          }
          """
      And The body of the response is the following
          """
          {"status":"ok"}
          """
     When I terminate Insights Results Aggregator
     Then Insights Results Aggregator process should terminate
