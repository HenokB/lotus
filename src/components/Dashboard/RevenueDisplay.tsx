import React, { useEffect, useState } from "react";
import { RevenueType } from "../../types/revenue-type";
import { GetRevenue } from "../../api/api";
import { Statistic, Card } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";
import { useQuery, UseQueryResult } from "react-query";
import LoadingSpinner from "../LoadingSpinner";

const computePercentageChange = (
  current: number | undefined,
  previous: number | undefined
): number => {
  if (previous === 0 || current === undefined || previous === undefined) {
    return 0;
  }
  return ((current - previous) / previous) * 100;
};

function RevenueDisplay(props: {
  total_revenue_1: number | undefined;
  total_revenue_2: number | undefined;
  isLoading: boolean;
}) {
  const [percentageChange, setPercentageChange] = useState<number>(0);
  useEffect(() => {
    setPercentageChange(
      computePercentageChange(props.total_revenue_1, props.total_revenue_2)
    );
  }, [props.total_revenue_1, props.total_revenue_2]);
  if (
    props.isLoading ||
    props.total_revenue_1 === undefined ||
    props.total_revenue_2 === undefined
  ) {
    return (
      <div>
        <LoadingSpinner />
      </div>
    );
  }
  return (
    <div className="px-2 py-2">
      <h1 className="text-xl font-main mb-4">Revenue</h1>
      <div className="grid grid-flow-col auto-cols-auto	 justify-between">
        <h2 className="text-3xl">$ {props.total_revenue_1}</h2>
        <div>
          {percentageChange >= 0 ? (
            <Statistic
              value={percentageChange}
              valueStyle={{
                color: "#3f8600",
                fontSize: "1.875rem",
                lineHeight: "2.25rem",
              }}
              precision={2}
              suffix="%"
              className="text-3xl"
            />
          ) : (
            <Statistic
              value={percentageChange}
              valueStyle={{
                color: "#cf1322",
              }}
              precision={2}
              suffix="%"
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default RevenueDisplay;
