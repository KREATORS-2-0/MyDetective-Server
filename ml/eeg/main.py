'''
Run the lie_analyzer class and the data obtained from it through
the ML model.
'''


from lie_analyzer import LieAnalyzer

if __name__ == "__main__":
    analyzer = LieAnalyzer()
    try:
        analyzer.start_streaming()
        analyzer.append_data()
        analyzer.stop_streaming()
        analyzer.analyze()
        print(analyzer.analysis_result)
    except KeyboardInterrupt:
        analyzer.stop_streaming()
    finally:
        analyzer.stop_streaming()