# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


import boto3
import os
import awswrangler as wr
import awswrangler.pandas as pd
from langchain_community.embeddings import BedrockEmbeddings 
from langchain_community.llms import Bedrock

#connect to the Model using bedrock API
bedrock_client = boto3.client(service_name="bedrock-runtime");
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)
#read the datset into memory
s3_input_url = os.environ.get('INPUT_BUCKET_URL');
s3_bucket_name = os.environ.get('BUCKET_NAME');
df = wr.s3.read_csv(path=s3_input_url)
#apply embedding to each product
df['embedding'] = df['product_name'].apply(bedrock_embeddings.embed_query);
#write the result
s3_output_url = f"s3://{s3_bucket_name}/embeddings.csv"
wr.s3.to_csv(df, s3_output_url,",",index=False);

exit(0);    