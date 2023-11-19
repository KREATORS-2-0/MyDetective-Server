from lie_analyzer import LieAnalyzer

if __name__ == "__main__":
    analyzer = LieAnalyzer()

    analyzer.start_streaming()
    analyzer.append_data()
    analyzer.stop_streaming()
    analyzer.analyze()
    print(analyzer.analysis_result)