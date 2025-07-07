CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wextra

SRCDIR := src
OBJDIR := obj

TARGET := qcomm
RCG_TARGET := rcg

MODULES := main architecture noc circuit communication communication_time core gate mapping parameters statistics utils simulation command_line
RCG_MODULES := rcg circuit gate utils

OBJS := $(addprefix $(OBJDIR)/, $(addsuffix .o, $(MODULES)))
RCG_OBJS := $(addprefix $(OBJDIR)/, $(addsuffix .o, $(RCG_MODULES)))

DEPS := $(OBJS:.o=.d)
RCG_DEPS := $(RCG_OBJS:.o=.d)

all: $(TARGET) $(RCG_TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(RCG_TARGET): $(RCG_OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -MMD -MP -c $< -o $@

-include $(DEPS)
-include $(RCG_DEPS)

clean:
	rm -rf $(OBJDIR) $(TARGET) $(RCG_TARGET)

rebuild: clean all

.PHONY: all clean rebuild