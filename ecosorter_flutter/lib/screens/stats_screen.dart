import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class StatsScreen extends StatelessWidget {
  const StatsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Estadísticas")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: BarChart(
          BarChartData(
            alignment: BarChartAlignment.spaceAround,
            maxY: 100,
            barGroups: [
              BarChartGroupData(x: 0, barRods: [
                BarChartRodData(toY: 60, width: 20, color: Colors.green)
              ], showingTooltipIndicators: [0]),
              BarChartGroupData(x: 1, barRods: [
                BarChartRodData(toY: 30, width: 20, color: Colors.blue)
              ], showingTooltipIndicators: [0]),
              BarChartGroupData(x: 2, barRods: [
                BarChartRodData(toY: 80, width: 20, color: Colors.orange)
              ], showingTooltipIndicators: [0]),
            ],
            titlesData: FlTitlesData(
              bottomTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  getTitlesWidget: (value, meta) {
                    switch (value.toInt()) {
                      case 0:
                        return const Text('Plástico');
                      case 1:
                        return const Text('Papel');
                      case 2:
                        return const Text('Vidrio');
                      default:
                        return const Text('');
                    }
                  },
                ),
              ),
              leftTitles: AxisTitles(
                sideTitles: SideTitles(showTitles: true),
              ),
            ),
            gridData: FlGridData(show: true),
            borderData: FlBorderData(show: false),
          ),
        ),
      ),
    );
  }
}
