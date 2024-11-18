To run the sender:
python3 -m stock-price-feeder | nc -lk 9999

To run the listener:
nc -lk localhost 9999 | python3 -m trader_apple
or
nc -lk localhost 9999 | python3 -m trader_msft


References:
1. https://www.google.com/search?q=how+to+calculate+the+average+of+elements+in+every+10+rows+in+a+pandas+dataframe&rlz=1C5GCCM_en&oq=how+to+calculate+the+average+of+elements+in+every+10+rows+in+a+pandas+dataframe&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRiPAtIBCTI4MzM0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
2. https://stackoverflow.com/questions/36810595/calculate-average-of-every-x-rows-in-a-table-and-create-new-table
3. https://www.google.com/search?q=python+dataframe+select+everything+but+the+first+10+elements+in+a+column&rlz=1C5GCCM_en&oq=python+dataframe+select+everything+but+the+first+10+elements+in+a+column&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTI0NjcxajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
4. https://stackoverflow.com/questions/74787113/combining-series-into-pandas-dataframes-ignoring-the-indices
5. https://stackoverflow.com/questions/18062135/combining-two-series-into-a-dataframe-in-pandas
6. chatGPT's instructions on how to use window in pysaprk
7. https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.withWatermark.html
8. https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#window-operations-on-event-time
9. https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.groupBy.html
10. https://www.linkedin.com/pulse/dealing-data-missing-dates-pyspark-neha-aggarwal/
11. https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.window.html
