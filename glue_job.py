import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import gs_derived
from pyspark.sql import functions as SqlFuncs

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1719265558667 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://tech-challenge-2/raw_data/"], "recurse": True}, transformation_ctx="AmazonS3_node1719265558667")

# Script generated for node Aggregate
Aggregate_node1719267560128 = sparkAggregate(glueContext, parentFrame = AmazonS3_node1719265558667, groups = ["date", "cod_acao"], aggs = [["qtd_acao", "max"]], transformation_ctx = "Aggregate_node1719267560128")

# Script generated for node Rename Field
RenameField_node1719270814013 = RenameField.apply(frame=Aggregate_node1719267560128, old_name="`max(qtd_acao)`", new_name="qtd_max_acao", transformation_ctx="RenameField_node1719270814013")

# Script generated for node Rename Field
RenameField_node1719272698535 = RenameField.apply(frame=RenameField_node1719270814013, old_name="cod_acao", new_name="codigo_acao", transformation_ctx="RenameField_node1719272698535")

# Script generated for node Rename Field
RenameField_node1719273626537 = RenameField.apply(frame=RenameField_node1719272698535, old_name="date", new_name="dia_mes_ano", transformation_ctx="RenameField_node1719273626537")

# Script generated for node Derived Column
DerivedColumn_node1719273593759 = RenameField_node1719273626537.gs_derived(colName="nova_data", expr="add_months(current_date(), 10)")

# Script generated for node Amazon S3
AmazonS3_node1719274399403 = glueContext.getSink(path="s3://tech-challenge-2/refined/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["dia_mes_ano", "codigo_acao"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1719274399403")
AmazonS3_node1719274399403.setCatalogInfo(catalogDatabase="tech-challenge",catalogTableName="pregao_com_data")
AmazonS3_node1719274399403.setFormat("glueparquet", compression="snappy")
AmazonS3_node1719274399403.writeFrame(DerivedColumn_node1719273593759)
job.commit()