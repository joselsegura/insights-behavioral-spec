# Copyright © 2021, 2022 Pavel Tisnovsky, Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database-related operations performed by BDD tests."""
from psycopg2.errors import UndefinedTable
from src.sql import construct_insert_statement
from behave import given, then, when
from common_aggregator import DB_TABLES


@given("the database is empty")
@then("the database is empty")
@then("I should find that the database is empty")
def ensure_database_emptiness(context):
    """Perform check if the database is empty."""
    cursor = context.connection.cursor()
    for table in DB_TABLES:
        try:
            cursor.execute(f"SELECT 1 from {table}")
            _ = cursor.fetchone()
            context.connection.commit()
            print("DB name: ", context.connection.info.dsn_parameters)
            raise Exception(f"Table '{table}' exists")
        except UndefinedTable:
            # exception means that the table does not exists
            context.connection.rollback()


@then("I should find that all tables are empty")
def ensure_data_tables_emptiness(context):
    """Perform check if data tables are empty."""
    for table in DB_TABLES:
        cursor = context.connection.cursor()
        try:
            cursor.execute(f"SELECT count(*) as cnt from {table}")
            results = cursor.fetchone()
            assert len(results) == 1, f"Wrong number of records returned: {len(results)}"
            assert results[0] == 0, f"Table '{table}' is not empty as expected"
        except Exception:
            raise


@when("I delete all tables from database")
def delete_all_tables(context):
    """Delete all relevant tables from database."""
    for table in DB_TABLES:
        cursor = context.connection.cursor()
        try:
            cursor.execute(f"DROP TABLE {table}")
            context.connection.commit()
        except Exception:
            context.connection.rollback()
            raise


@when("I insert following records into {table} table")
def insert_records_into_selected_table(context, table):
    """Insert provided records into specified table."""
    cursor = context.connection.cursor()

    try:
        headings = context.table.headings

        # construct INSERT statement
        insert_statement = construct_insert_statement(table, headings)

        # perform several INSERTs
        for row in context.table:
            # try to perform INSERT statement
            print(row)
            cursor.execute(insert_statement, row)

        context.connection.commit()
    except Exception:
        context.connection.rollback()
        raise
